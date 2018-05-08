# -*- coding: utf-8 -*-

"""
This module populates the tables of bio2bel_reactome
"""

import itertools as itt
import logging
from collections import Counter

from compath_utils import CompathManager
from tqdm import tqdm

from bio2bel_chebi.manager import Manager as ChebiManager
from bio2bel_hgnc.manager import Manager as HgncManager
from .constants import MODULE_NAME
from .models import Base, Chemical, Pathway, Protein, Species
from .parsers import *

log = logging.getLogger(__name__)

__all__ = [
    'Manager'
]


class Manager(CompathManager):
    """Bio2BEL Reactome manager."""

    module_name = MODULE_NAME
    pathway_model = Pathway
    protein_model = Protein
    pathway_model_identifier_column = Pathway.reactome_id

    has_hierarchy = True  # Indicates that this manager can handle hierarchies with the Pathway Model

    def __init__(self, connection=None):
        super().__init__(connection=connection)

        # Global dictionary
        self.pid_protein = {}

    @property
    def _base(self):
        return Base

    def count_pathways(self):
        """Counts the pathways in the database

        :rtype: int
        """
        return self.session.query(Pathway).count()

    def count_chemicals(self):
        """Counts the chemicals in the database

        :rtype: int
        """
        return self.session.query(Chemical).count()

    def count_proteins(self):
        """Counts the proteins in the database

        :rtype: int
        """
        return self.session.query(Protein).count()

    def count_species(self):
        """Counts the species in the database

        :rtype: int
        """
        return self.session.query(Species).count()

    """Custom query methods"""

    def query_gene_set(self, gene_set):
        """Returns pathway counter dictionary

        :param list[str] gene_set: gene set to be queried
        :rtype: dict[str,dict]]
        :return: Enriched pathways with mapped pathways/total
        """
        proteins = self._query_proteins_in_hgnc_list(gene_set)

        pathways_lists = [
            protein.get_pathways_ids()
            for protein in proteins
        ]

        # Flat the pathways lists and applies Counter to get the number matches in every mapped pathway
        pathway_counter = Counter(itt.chain(*pathways_lists))

        enrichment_results = dict()

        for pathway_reactome_id, proteins_mapped in pathway_counter.items():
            pathway = self.get_pathway_by_id(pathway_reactome_id)

            pathway_gene_set = pathway.get_gene_set()  # Pathway gene set

            enrichment_results[pathway.reactome_id] = {
                "pathway_id": pathway.reactome_id,
                "pathway_name": pathway.name,
                "mapped_proteins": proteins_mapped,
                "pathway_size": len(pathway_gene_set),
                "pathway_gene_set": pathway_gene_set,
            }

        return enrichment_results

    def export_genesets(self, species=None, top_hierarchy=None):
        """Returns pathway - genesets mapping

        :param opt[str] species: pathways specific to a species
        :param opt[bool] top_hierarchy: extract only the top hierarchy pathways
        :rtype: dict[set]
        :return: pathways' genesets
        """

        if species:
            return {
                pathway.name: {
                    protein.hgnc_symbol
                    for protein in pathway.proteins
                }
                for pathway in self.session.query(Pathway).all()
                if pathway.species.name == species
            }

        if top_hierarchy:
            return {
                pathway.name: {
                    protein.hgnc_symbol
                    for protein in pathway.proteins
                }
                for pathway in self.session.query(Pathway).all()
                if not pathway.parent_id
            }

        # if no species and not top hierarchy return all
        return {
            pathway.name: {
                protein.hgnc_symbol
                for protein in pathway.proteins
            }
            for pathway in self.session.query(Pathway).all()
        }

    def get_or_create_pathway(self, reactome_id, name, species):
        """Gets an pathway from the database or creates it

        :param str reactome_id: pathway identifier
        :param str name: name of the pathway
        :param bio2bel_reactome.models.Species species: Species object
        :rtype: Pathway
        """
        pathway = self.get_pathway_by_id(reactome_id)

        if pathway is None:
            pathway = Pathway(
                reactome_id=reactome_id,
                name=name,
                species=species
            )
            self.session.add(pathway)

        return pathway

    def get_or_create_chemical(self, chebi_id, chebi_name):
        """Gets a Chemical from the database or creates it

        :param str chebi_id: identifier
        :param str chebi_name: name
        :rtype: Chemical
        """
        chemical = self.get_chemical_by_chebi_id(chebi_id)

        if chemical is None:
            chemical = Chemical(
                chebi_id=chebi_id,
                chebi_name=chebi_name
            )

            self.session.add(chemical)

        return chemical

    def get_or_create_species(self, species_name):
        """Gets an Species from the database or creates it

        :param str species_name: name
        :rtype: Species
        """
        species = self.get_species_by_name(species_name)

        if species is None:
            species = Species(
                name=species_name,
            )
            self.session.add(species)

        return species

    def get_or_create_protein(self, uniprot_id, hgnc_symbol=None, hgnc_id=None):
        """Gets an protein from the database or creates it

        :param str uniprot_id: pathway identifier
        :param Optional[str] hgnc_symbol: name of the pathway
        :param Optional[str] hgnc_id: Species object
        :rtype: Protein
        """
        protein = self.get_protein_by_uniprot_id(uniprot_id)

        if protein is not None:
            return protein

        protein = self.pid_protein.get(uniprot_id)

        if protein is not None:
            self.session.add(protein)
            return protein

        protein = self.pid_protein[uniprot_id] = Protein(
            uniprot_id=uniprot_id,
            hgnc_symbol=hgnc_symbol,
            hgnc_id=hgnc_id
        )
        self.session.add(protein)

        return protein

    def get_species_by_name(self, species_name):
        """Gets a Species by its species_name

        :param str species_name: name
        :rtype: Optional[Species]
        """
        return self.session.query(Species).filter(Species.name == species_name).one_or_none()

    def get_pathway_names_to_ids(self):
        """Returns a dictionary of pathway names to ids

        :rtype: dict[str,str]
        """
        human_pathways = self.get_pathways_by_species('Homo sapiens')

        return {
            pathway.name: pathway.reactome_id
            for pathway in human_pathways
        }

    def get_all_hgnc_symbols(self):
        """Returns the set of genes present in all Reactome Pathways

        :rtype: set
        """
        return {
            gene.hgnc_symbol
            for pathway in self.get_pathways_by_species('Homo sapiens')
            for gene in pathway.proteins
            if pathway.proteins
        }

    def get_pathway_size_distribution(self):
        """Returns pathway sizes

        :rtype: dict
        :return: pathway sizes
        """

        pathways = self.get_pathways_by_species('Homo sapiens')

        return {
            pathway.name: len(pathway.proteins)
            for pathway in pathways
            if pathway.proteins
        }

    def get_pathway_by_name(self, pathway_name, species=None):
        """Gets a pathway by name

        :param pathway_name: name
        :param Optional[str] species: name
        :rtype: Optional[Pathway]
        """
        results = self.session.query(Pathway).filter(Pathway.name == pathway_name).all()

        if not results:
            return None

        if not species:
            species = 'Homo sapiens'

        for pathway in results:

            if pathway.species.name == species:
                return pathway

        return None

    def get_pathway_parent_by_id(self, reactome_id):
        """Gets parent pathway by its reactome id

        :param reactome_id: reactome identifier
        :rtype: Optional[Pathway]
        """
        pathway = self.get_pathway_by_id(reactome_id)

        if not pathway or not pathway.parent:
            return None

        return pathway.parent

    def get_top_hiearchy_parent_by_id(self, reactome_id):
        """Gets the oldest pathway at the top of the hierarchy a pathway by its reactome id

        :param reactome_id: reactome identifier
        :rtype: Optional[Pathway]
        """

        pathway = self.get_pathway_by_id(reactome_id)

        if not pathway.parent:
            return pathway

        return self.get_top_hiearchy_parent_by_id(pathway.parent.reactome_id)

    def get_all_top_hierarchy_pathways(self):
        """Gets all pathways without a parent (top hierarchy)

        :rtype: list[Pathways]
        """
        all_pathways = self.get_all_pathways()

        return [
            pathway
            for pathway in all_pathways
            if not pathway.parent_id
        ]
    
    def get_all_pathway_names(self):
        """Gets all pathway names stored in the database

        :rtype: list[str]
        """
        return [
            pathway.name
            for pathway in self.session.query(self.pathway_model).all()
            if pathway.species.name == 'Homo sapiens'
        ]

    def get_pathways_by_species(self, species_name):
        """Gets pathways by species"""
        filtered_species = self.session.query(Species).filter(Species.name == species_name).one_or_none()

        if not filtered_species:
            return None

        return filtered_species.pathways

    def get_chemical_by_chebi_id(self, chebi_id):
        """Gets chemical by CHEBI id"""
        return self.session.query(Chemical).filter(Chemical.chebi_id == chebi_id).one_or_none()

    def get_protein_by_uniprot_id(self, uniprot_id):
        """Gets protein by UniProt id"""
        return self.session.query(Protein).filter(Protein.uniprot_id == uniprot_id).one_or_none()

    """Custom Methods to Populate the DB"""

    def _populate_pathways(self, url=None):
        """ Populate pathway table

        :param url: Optional[str] url: url from pathway table file
        """

        df = get_pathway_names_df(url=url)
        pathways_dict, species_set = parse_pathway_names(df)

        species_name_to_model = {}

        log.info("populating species")

        for species_name in tqdm(species_set, desc='Loading species'):
            new_species = self.get_or_create_species(species_name)
            species_name_to_model[species_name] = new_species

        log.info("populating pathways")

        for reactome_id, (name, species) in tqdm(pathways_dict.items(), desc='Loading pathways'):
            pathway = self.get_or_create_pathway(
                reactome_id=reactome_id,
                name=name,
                species=species_name_to_model[species]
            )

            self.session.add(pathway)

        self.session.commit()

    def _pathway_hierarchy(self, url=None):
        """ Links pathway models through hierarchy

        :param Optional[str] url: url from pathway hierarchy file
        """
        df = get_pathway_hierarchy_df(url=url)
        pathways_hierarchy = parse_pathway_hierarchy(df)

        log.info("populating pathway hierarchy")

        for parent_id, child_id in tqdm(pathways_hierarchy, desc='Loading pathway hierarchy'):
            if parent_id is None:
                log.warning('parent id is None')
                continue

            if child_id is None:
                log.warning('child id is None')
                continue

            parent = self.get_pathway_by_id(parent_id)
            child = self.get_pathway_by_id(child_id)

            parent.children.append(child)

        self.session.commit()

    def _pathway_protein(self, hgnc_manager, url=None, only_human=True):
        """Populates UniProt Tables

        :param bio2bel_hgnc.manager.Manager hgnc_manager: Hgnc Manager.
        :param Optional[str] url: url from pathway protein file
        :param bool url: only_human: only store human genes. Defaults to True.
        """

        log.warning(
            "downloading proteins. This might take a couple of minutes depending on your internet connection..."
        )

        uniprot_df = get_proteins_pathways_df(url=url)
        uniprots = parse_entities_pathways(entities_pathways_df=uniprot_df, only_human=only_human)

        log.info("populating protein data")
        missing_reactome_ids = set()
        missing_hgnc_info = set()

        for uniprot_id, reactome_id, evidence in tqdm(uniprots, desc='Loading proteins'):

            if uniprot_id is None:
                log.warning('Uniprot identifier is None')
                continue

            genes = get_hgnc_symbol_id_by_uniprot_id(hgnc_manager, uniprot_id)

            if not genes:

                log.debug('{} has no HGNC info'.format(uniprot_id))
                missing_hgnc_info.add(uniprot_id)

                protein = self.get_or_create_protein(uniprot_id=uniprot_id)

            # Human gene is stored with additional info
            else:
                for gene in genes:
                    protein = self.get_or_create_protein(
                        uniprot_id=uniprot_id,
                        hgnc_symbol=gene.symbol,
                        hgnc_id=gene.identifier
                    )

            pathway = self.get_pathway_by_id(reactome_id)

            if pathway is None:
                log.warning('Missing reactome identifier: %s', reactome_id)
                missing_reactome_ids.add(reactome_id)
                continue

            if pathway not in protein.pathways:
                protein.pathways.append(pathway)

        self.session.commit()

        if missing_reactome_ids:
            log.warning('missing %d reactome ids', len(missing_reactome_ids))

        if missing_hgnc_info:
            log.warning('missing %d hgncs', len(missing_hgnc_info))

    def _pathway_chemical(self, chebi_manager, url=None, only_human=True):
        """ Populates Chebi Tables

        :param bio2bel_chebi.manager.Manager chebi_manager: Chebi Manager
        :param url: Optional[str] url: url from pathway chemical file
        :param bool only_human: only store human chemicals
        """

        log.info("downloading chemicals")

        chebi_df = get_chemicals_pathways_df(url=url)
        chebis = parse_entities_pathways(entities_pathways_df=chebi_df, only_human=only_human)

        log.info("populating chemicals")
        cid_chemical = {}
        missing_reactome_ids = set()

        for chebi_id, reactome_id, evidence in tqdm(chebis, desc='Loading chemicals'):
            if chebi_id is None:
                log.debug('ChEBI identifier is None')
                continue

            if chebi_id in cid_chemical:
                chemical = cid_chemical[chebi_id]

            else:
                chebi_chemical = chebi_manager.get_chemical_by_chebi_id(chebi_id)

                if chebi_chemical is None:
                    log.warning('{} was not found by chebi manager'.format(chebi_id))
                    continue

                chemical = self.get_or_create_chemical(chebi_id, chebi_chemical.name)
                cid_chemical[chebi_id] = chemical

            pathway = self.get_pathway_by_id(reactome_id)

            if pathway is None:
                log.debug('Missing reactome_id: %s', reactome_id)
                missing_reactome_ids.add(reactome_id)
                continue

            if pathway not in chemical.pathways:
                chemical.pathways.append(pathway)

        if missing_reactome_ids:
            log.warning('missing %d reactome ids', len(missing_reactome_ids))

        self.session.commit()

    def populate(
            self,
            hgnc_manager=None,
            chebi_manager=None,
            pathways_path=None,
            pathways_hierarchy_path=None,
            pathways_proteins_path=None,
            pathways_chemicals_path=None,
            only_human=True
    ):

        """ Populates all tables

        :param bio2bel_hgnc.manager.Manager hgnc_manager: Hgnc Manager
        :param bio2bel_chebi.manager.Manager chebi_manager: Chebi Manager
        :param pathways_path: Optional[str] url: url from pathway table file
        :param pathways_hierarchy_path: Optional[str] url: url from pathway hierarchy file
        :param pathways_proteins_path: Optional[str] url: url from pathway protein file
        :param pathways_chemicals_path: Optional[str] url: url from pathway chemical file
        :param bool only_human: only store human chemicals
        """
        self._populate_pathways(url=pathways_path)
        self._pathway_hierarchy(url=pathways_hierarchy_path)

        hgnc_m = HgncManager.ensure(hgnc_manager)
        chebi_m = ChebiManager.ensure(chebi_manager)

        self._pathway_protein(hgnc_manager=hgnc_m, url=pathways_proteins_path, only_human=only_human)
        self._pathway_chemical(chebi_manager=chebi_m, url=pathways_chemicals_path, only_human=only_human)

    def _add_admin(self, app, **kwargs):
        from flask_admin import Admin
        from flask_admin.contrib.sqla import ModelView

        class PathwayView(ModelView):
            """Pathway view in Flask-admin"""
            column_searchable_list = (
                Pathway.reactome_id,
                Pathway.name,
            )

        class ProteinView(ModelView):
            """Protein view in Flask-admin"""
            column_searchable_list = (
                Protein.hgnc_symbol,
                Protein.uniprot_id,
                Protein.hgnc_id
            )

        class SpeciesView(ModelView):
            """Species view in Flask-admin"""
            column_searchable_list = (
                Species.name,
            )

        class ChemicalView(ModelView):
            """Chemical view in Flask-admin"""
            column_searchable_list = (
                Chemical.chebi_id,
            )

        admin = Admin(app, **kwargs)
        admin.add_view(PathwayView(Pathway, self.session))
        admin.add_view(ProteinView(Protein, self.session))
        admin.add_view(ChemicalView(Chemical, self.session))
        admin.add_view(SpeciesView(Species, self.session))
        return admin
