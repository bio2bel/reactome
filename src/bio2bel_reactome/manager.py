# -*- coding: utf-8 -*-

"""This module populates the tables of bio2bel_reactome."""

import logging
from collections import Counter, defaultdict
from typing import Dict, List, Mapping, Optional, Set

import itertools as itt
import pandas as pd
from sqlalchemy import and_
from tqdm import tqdm

from bio2bel.manager.compath import CompathManager
from pybel import BELGraph
from pyobo import get_name_id_mapping
from .constants import MODULE_NAME, SPECIES_REMAPPING
from .models import Base, Chemical, Pathway, Protein, Species, chemical_pathway, protein_pathway
from .parsers import (
    get_pathway_hierarchy_df, get_pathway_names_df, get_procesed_chemical_pathways_df,
    get_procesed_proteins_pathways_df, parse_pathway_hierarchy, parse_pathway_names,
)

logger = logging.getLogger(__name__)

__all__ = [
    'Manager',
]


class Manager(CompathManager):
    """Protein-pathway and chemical-pathway memberships."""

    module_name = MODULE_NAME
    protein_model = Protein
    _base = Base
    edge_model = [protein_pathway, chemical_pathway]
    namespace_model = pathway_model = Pathway
    flask_admin_models = [Pathway, Protein, Species, Chemical]

    has_hierarchy = True  # Indicates that this manager can handle hierarchies with the Pathway Model

    def __init__(self, *args, only_human: bool = False, **kwargs):
        super().__init__(*args, **kwargs)
        self.only_human = only_human
        # Global dictionary
        self.uniprot_id_to_protein: Dict[str, Protein] = {}
        self.chebi_id_to_chemical: Dict[str, Chemical] = {}

    def summarize(self) -> Mapping[str, int]:
        """Summarize the database."""
        return dict(
            pathways=self.count_pathways(),
            proteins=self.count_proteins(),
            chemicals=self.count_chemicals(),
            species=self.count_species(),
        )

    def count_pathways(self) -> int:
        """Count the pathways in the database."""
        return self.session.query(Pathway).count()

    def count_chemicals(self) -> int:
        """Count the chemicals in the database."""
        return self.session.query(Chemical).count()

    def count_proteins(self) -> int:
        """Count the proteins in the database."""
        return self.session.query(Protein).count()

    def count_species(self) -> int:
        """Count the species in the database."""
        return self.session.query(Species).count()

    """Custom query methods"""

    def query_similar_pathways(self, pathway_name: str, top: Optional[int] = None) -> List[Pathway]:
        """Filter pathways by name.

        :param pathway_name: pathway name to query
        :param top: return only X entries
        """
        query = self.session.query(self.pathway_model.identifier, self.pathway_model.name)

        if self.only_human:
            _filter = and_(
                self.pathway_model.name.contains(pathway_name),
                Species.name == 'Homo sapiens',
            )
            query = query.join(Species).filter(_filter)

        else:
            _filter = self.pathway_model.name.contains(pathway_name)
            query = query.filter(_filter)

        if top is None:
            return query.all()

        return query.limit(top).all()

    def query_gene_set(self, gene_set):
        """Return pathway counter dictionary.

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

    def export_gene_sets(
        self,
        top_hierarchy: Optional[bool] = None,
    ) -> Mapping[str, Set[str]]:
        """Return pathway - genesets mapping

        :param species: pathways specific to a species
        :param top_hierarchy: extract only the top hierarchy pathways
        :rtype: dict[set]
        :return: pathways' genesets
        """
        if self.only_human:
            pathways = self.get_human_pathways()
            return {
                pathway.name: {
                    protein.hgnc_symbol
                    for protein in pathway.proteins
                    if protein.hgnc_symbol
                }
                for pathway in pathways
                if pathway.proteins
            }

        if top_hierarchy:
            return {
                pathway.name: {
                    protein.hgnc_symbol
                    for protein in pathway.proteins
                    if protein.hgnc_symbol
                }
                for pathway in self.get_all_pathways()
                if not pathway.parent_id and pathway.proteins
            }

        # if no species and not top hierarchy return all
        return {
            pathway.name: {
                protein.hgnc_symbol
                for protein in pathway.proteins
                if protein.hgnc_symbol
            }
            for pathway in self.get_all_pathways()
            if pathway.proteins
        }

    def get_gene_distribution(self):
        """Return the proteins in the database within the gene set query.

        :rtype: collections.Counter
        :return: pathway sizes
        """
        return Counter(
            protein.hgnc_symbol
            for pathway in self.get_all_pathways()
            if pathway.proteins
            for protein in pathway.proteins
            if protein.hgnc_symbol
        )

    def get_gene_sets(self) -> Mapping[str, Set[str]]:
        """Return pathway - genesets mapping."""
        if self.only_human:
            pathways = self.get_human_pathways()
        else:
            pathways = self.get_all_pathways()

        return {
            pathway.name: {
                protein.hgnc_symbol
                for protein in pathway.proteins
                if protein.hgnc_symbol
            }
            for pathway in pathways
            if pathway.proteins
        }

    def get_or_create_pathway(
        self,
        *,
        reactome_id: str,
        name: str,
        species: Species,
        chemicals: Optional[List[Chemical]],
    ) -> Pathway:
        """Get a pathway from the database or creates it.

        :param reactome_id: pathway identifier
        :param name: name of the pathway
        :param species: Species object
        """
        pathway = self.get_pathway_by_id(reactome_id)

        if pathway is None:
            pathway = Pathway(
                identifier=reactome_id,
                name=name,
                species=species,
                chemicals=chemicals,
            )
            self.session.add(pathway)

        return pathway

    def get_or_create_chemical(self, *, chebi_id: str, chebi_name: str) -> Chemical:
        """Get a Chemical from the database or creates it.

        :param chebi_id: identifier
        :param chebi_name: name
        """
        chemical = self.get_chemical_by_chebi_id(chebi_id)

        if chemical is None:
            chemical = Chemical(
                chebi_id=chebi_id,
                name=chebi_name,
            )
            self.session.add(chemical)

        return chemical

    def get_or_create_species(self, *, taxonomy_id: str, name: str) -> Species:
        """Get a Species from the database or creates it."""
        species = self.get_species_by_name(name)

        if species is None:
            species = Species(taxonomy_id=taxonomy_id, name=name)
            self.session.add(species)

        return species

    def get_or_create_protein(
        self,
        uniprot_id: str,
        hgnc_symbol: Optional[str] = None,
        hgnc_id: Optional[str] = None,
    ) -> Protein:
        """Get a protein from the database or creates it.

        :param uniprot_id: pathway identifier
        :param hgnc_symbol: name of the pathway
        :param hgnc_id: Species object
        """
        protein = self.get_protein_by_uniprot_id(uniprot_id)

        if protein is not None:
            return protein

        protein = self.uniprot_id_to_protein.get(uniprot_id)

        if protein is not None:
            self.session.add(protein)
            return protein

        protein = self.uniprot_id_to_protein[uniprot_id] = Protein(
            uniprot_id=uniprot_id,
            hgnc_symbol=hgnc_symbol,
            hgnc_id=hgnc_id,
        )
        self.session.add(protein)

        return protein

    def get_species_by_name(self, species_name: str) -> Optional[Species]:
        """Get a Species by its species_name.

        :param species_name: name
        """
        return self.session.query(Species).filter(Species.name == species_name).one_or_none()

    def get_pathway_names_to_ids(self):
        """Return a dictionary of pathway names to ids

        :rtype: dict[str,str]
        """
        if self.only_human:
            pathways = self.get_human_pathways()
        else:
            pathways = self.get_all_pathways()

        return {
            pathway.name: pathway.identifier
            for pathway in pathways
        }

    def get_all_hgnc_symbols(self):
        """Return the set of genes present in all Reactome Pathways.

        :rtype: set
        """
        return {
            gene.hgnc_symbol
            for pathway in self.get_human_pathways()
            for gene in pathway.proteins
            if pathway.proteins
        }

    def get_pathway_size_distribution(self):
        """Return pathway sizes.

        :rtype: dict
        :return: pathway sizes
        """
        if self.only_human:
            pathways = self.get_human_pathways()
        else:
            pathways = self.get_all_pathways()

        return {
            pathway.identifier: (pathway.name, len(pathway.proteins))
            for pathway in pathways
            if pathway.proteins
        }

    def get_pathway_by_name(self, pathway_name: str, species_name: Optional[str] = None) -> Optional[Pathway]:
        """Get a pathway by name."""
        results = self.session.query(Pathway).filter(Pathway.name == pathway_name).all()

        if not results:
            return None

        if not species_name:
            species_name = 'Homo sapiens'

        for pathway in results:
            if pathway.species.name == species_name:
                return pathway

        return None

    def get_pathway_parent_by_id(self, reactome_id: str) -> Optional[Pathway]:
        """Get parent pathway by its reactome id.

        :param reactome_id: reactome identifier
        """
        pathway = self.get_pathway_by_id(reactome_id)

        if not pathway or not pathway.parent:
            return None

        return pathway.parent

    def get_top_hiearchy_parent_by_id(self, reactome_id: str) -> Optional[Pathway]:
        """Get the oldest pathway at the top of the hierarchy a pathway by its reactome id.

        :param reactome_id: reactome identifier
        """
        pathway = self.get_pathway_by_id(reactome_id)

        if not pathway.parent:
            return pathway

        return self.get_top_hiearchy_parent_by_id(pathway.parent.reactome_id)

    def get_all_top_hierarchy_pathways(self) -> List[Pathway]:
        """Get all pathways without a parent (top hierarchy)."""
        all_pathways = self.get_all_pathways()

        return [
            pathway
            for pathway in all_pathways
            if not pathway.parent_id
        ]

    def get_all_pathway_names(self) -> Set[str]:
        """Get all pathway names stored in the database."""
        return set(self.session.query(Pathway.name))

    def get_human_pathways(self) -> List[Pathway]:
        """Get human pathways."""
        return self.get_pathways_by_species('Homo sapiens')

    def get_pathways_by_species(self, species_name: str) -> Optional[List[Pathway]]:
        """Get pathways by species."""
        filtered_species = self.session.query(Species).filter(Species.name == species_name).one_or_none()

        if not filtered_species:
            return None

        return filtered_species.pathways

    def get_chemical_by_chebi_id(self, chebi_id: str) -> Optional[Chemical]:
        """Get chemical by CHEBI id."""
        return self.session.query(Chemical).filter(Chemical.chebi_id == chebi_id).one_or_none()

    def get_protein_by_uniprot_id(self, uniprot_id: str) -> Optional[Protein]:
        """Get protein by UniProt id."""
        return self.session.query(Protein).filter(Protein.uniprot_id == uniprot_id).one_or_none()

    def to_bel(self) -> BELGraph:
        """Serialize Reactome to BEL."""
        graph = BELGraph(
            name='Reactome Pathway Definitions',
            version='1.0.0',
        )
        for pathway in self.list_pathways():
            pathway.add_to_bel_graph(graph)
        return graph

    """Custom Methods to Populate the DB"""

    def _populate_pathways(
        self,
        chemical_mapping: Mapping[str, List[Chemical]],
        url: Optional[str] = None,
    ) -> None:
        """Populate the pathway table.

        :param url: url from pathway table file
        """
        df = get_pathway_names_df(url=url)
        pathways_dict, species_set = parse_pathway_names(df)

        species_name_to_id = get_name_id_mapping('ncbitaxon')
        species_name_to_model = {}

        for species_name in tqdm(species_set, desc='populating species'):
            species_name = SPECIES_REMAPPING.get(species_name, species_name)
            species_name_to_model[species_name] = self.get_or_create_species(
                name=species_name,
                taxonomy_id=species_name_to_id[species_name],
            )

        for reactome_id, (name, species_name) in tqdm(pathways_dict.items(), desc='populating pathways'):
            species_name = SPECIES_REMAPPING.get(species_name, species_name)

            pathway = self.get_or_create_pathway(
                reactome_id=reactome_id,
                name=name,
                species=species_name_to_model[species_name],
                chemicals=chemical_mapping.get(reactome_id),
            )
            self.session.add(pathway)

        self.session.commit()

    def _pathway_hierarchy(self, url=None):
        """ Links pathway models through hierarchy

        :param Optional[str] url: url from pathway hierarchy file
        """
        df = get_pathway_hierarchy_df(url=url)
        pathways_hierarchy = parse_pathway_hierarchy(df)

        for parent_id, child_id in tqdm(pathways_hierarchy, desc='populating pathway hierarchy'):
            if parent_id is None:
                logger.warning('parent id is None')
                continue

            if child_id is None:
                logger.warning('child id is None')
                continue

            parent = self.get_pathway_by_id(parent_id)
            child = self.get_pathway_by_id(child_id)

            parent.children.append(child)

        self.session.commit()

    def _pathway_protein(self, url: Optional[str] = None):
        """Populate UniProt tables.

        :param url: url from pathway protein file
        """
        rv = {}

        uniprot_df = get_procesed_proteins_pathways_df(url=url)
        if self.only_human:
            uniprot_df = uniprot_df[uniprot_df['species'] == 'Homo sapiens']

        missing_reactome_ids = set()
        missing_hgnc_info = set()

        protein_info_df = uniprot_df[['uniprot_id', 'uniprot_accession', 'hgnc_id', 'hgnc_symbol']].drop_duplicates()
        it = tqdm(protein_info_df.values, total=len(protein_info_df.index), descp='populating proteins')
        for uniprot_id, uniprot_accession, hgnc_id, hgnc_symbol in it:
            self.uniprot_id_to_protein[uniprot_id] = Protein(
                uniprot_id=uniprot_id,
                uniprot_accession=uniprot_accession,
                hgnc_id=hgnc_id,
                hgnc_symbol=hgnc_symbol,
            )

        it = tqdm(uniprot_df, desc='populating proteins-pathway relations')
        for uniprot_id, reactome_id, evidence in it:
            if uniprot_id is None:
                logger.debug('uniprot_id is none')
                continue

            protein = self.uniprot_id_to_protein[uniprot_id]
            pathway = self.get_pathway_by_id(reactome_id)
            if pathway is None:
                if reactome_id not in missing_reactome_ids:
                    it.write(f'protein/pathway mapping: could not find reactome:{reactome_id}')
                missing_reactome_ids.add(reactome_id)
                continue

            if pathway not in protein.pathways:
                protein.pathways.append(pathway)

        self.session.commit()

        if missing_reactome_ids:
            logger.warning('missing %d reactome ids', len(missing_reactome_ids))

        if missing_hgnc_info:
            logger.warning('missing %d hgncs', len(missing_hgnc_info))

    def _get_chemical_mapping(self, url: Optional[str] = None) -> Mapping[str, List[Chemical]]:
        """Populate ChEBI tables.

        :param url: url from pathway chemical file
        """
        chemical_pathways_df = get_procesed_chemical_pathways_df(url=url)
        if self.only_human:
            chemical_pathways_df = chemical_pathways_df[chemical_pathways_df['species'] == 'Homo sapiens']

        chemicals_df = chemical_pathways_df[['chebi_id', 'chebi_name']].drop_duplicates()
        it = tqdm(chemicals_df.values, total=len(chemicals_df.index), desc='populating chemicals')
        chebi_id_to_chemical = {}
        for chebi_id, chebi_name in it:
            if pd.isna(chebi_id):
                continue
            chebi_id_to_chemical[chebi_id] = Chemical(chebi_id=chebi_id, name=chebi_name)

        rv = defaultdict(list)
        _df = chemical_pathways_df[['chebi_id', 'reactome_id']].drop_duplicates().values
        it = tqdm(_df, total=len(_df.index), desc='populating chemical/reactome')
        for chebi_id, reactome_id in it:
            chemical = chebi_id_to_chemical[chebi_id]
            rv[reactome_id].append(chemical)
        return dict(rv)

    def populate(
        self,
        pathways_path: Optional[str] = None,
        pathways_hierarchy_path: Optional[str] = None,
        pathways_proteins_path: Optional[str] = None,
        pathways_chemicals_path: Optional[str] = None,
    ) -> None:
        """Populate all tables.

        :param pathways_path: url from pathway table file
        :param pathways_hierarchy_path: url from pathway hierarchy file
        :param pathways_proteins_path: url from pathway protein file
        :param pathways_chemicals_path: url from pathway chemical file
        """
        chemical_mapping = self._get_chemical_mapping(url=pathways_chemicals_path)
        self._populate_pathways(url=pathways_path, chemical_mapping=chemical_mapping)
        self._pathway_hierarchy(url=pathways_hierarchy_path)
        self._pathway_protein(url=pathways_proteins_path)

    def _add_admin(self, app, **kwargs):
        from flask_admin import Admin
        from flask_admin.contrib.sqla import ModelView

        class PathwayView(ModelView):
            """Pathway view in Flask-admin"""
            column_searchable_list = (
                Pathway.identifier,
                Pathway.name,
            )

        class ProteinView(ModelView):
            """Protein view in Flask-admin."""

            column_searchable_list = (
                Protein.hgnc_symbol,
                Protein.uniprot_id,
                Protein.hgnc_id,
            )

        class SpeciesView(ModelView):
            """Species view in Flask-admin."""

            column_searchable_list = (
                Species.taxonomy_id,
                Species.name,
            )

        class ChemicalView(ModelView):
            """Chemical view in Flask-admin."""

            column_searchable_list = (
                Chemical.chebi_id,
                Chemical.name,
            )

        admin = Admin(app, **kwargs)
        admin.add_view(PathwayView(Pathway, self.session))
        admin.add_view(ProteinView(Protein, self.session))
        admin.add_view(ChemicalView(Chemical, self.session))
        admin.add_view(SpeciesView(Species, self.session))
        return admin
