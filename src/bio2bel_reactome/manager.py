# -*- coding: utf-8 -*-

"""
This module populates the tables of bio2bel_reactome
"""

import configparser
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm

from bio2bel_reactome.constants import *
from bio2bel_reactome.models import Base, Chemical, Pathway, Protein, Species
from bio2bel_reactome.parsers import *

log = logging.getLogger(__name__)


class Manager(object):
    def __init__(self, connection=None):
        self.connection = self.get_connection(connection)
        self.engine = create_engine(self.connection)
        self.session_maker = sessionmaker(bind=self.engine, autoflush=False, expire_on_commit=False)
        self.session = self.session_maker()
        self.make_tables()

    @staticmethod
    def get_connection(connection=None):
        """Return the SQLAlchemy connection string if it is set
        :param connection: get the SQLAlchemy connection string
        :rtype: str
        """
        if connection:
            return connection

        config = configparser.ConfigParser()

        cfp = REACTOME_CONFIG_FILE_PATH

        if os.path.exists(cfp):
            log.info('fetch database configuration from {}'.format(cfp))
            config.read(cfp)
            connection = config['database']['sqlalchemy_connection_string']
            log.info('load connection string from {}: {}'.format(cfp, connection))
            return connection

        with open(cfp, 'w') as config_file:
            config['database'] = {'sqlalchemy_connection_string': REACTOME_SQLITE_PATH}
            config.write(config_file)
            log.info('create configuration file {}'.format(cfp))

        return REACTOME_SQLITE_PATH

    def make_tables(self, check_first=True):
        """Create tables"""
        log.info('create table in {}'.format(self.engine.url))
        Base.metadata.create_all(self.engine, checkfirst=check_first)

    def drop_tables(self):
        """drops all tables in the database"""
        log.info('drop tables in {}'.format(self.engine.url))
        Base.metadata.drop_all(self.engine)

    @staticmethod
    def ensure(connection=None):
        """Checks and allows for a Manager to be passed to the function. """
        if connection is None or isinstance(connection, str):
            return Manager(connection=connection)

        if isinstance(connection, Manager):
            return connection

        raise TypeError

    """Custom Methods to Populate the DB"""

    def get_pathway_by_id(self, reactome_id):
        """Gets a pathway by its reactome id

        :param reactome_id:
        :rtype: Optional[Pathway]
        """
        return self.session.query(Pathway).filter(Pathway.reactome_id == reactome_id).one_or_none()

    def _populate_pathways(self, url=None):
        """ Populate pathway table

        :param url: path or link to data source needed for get_data()
        """

        df = get_pathway_names_df(url=url)
        pathways_dict, species_set = parse_pathway_names(df)

        species_name_to_model = {}

        log.info("populating species")

        for species_name in tqdm(species_set, desc='Loading species'):
            new_species = Species(
                name=species_name,
            )

            self.session.add(new_species)
            species_name_to_model[species_name] = new_species

        rid_pathway = {}

        log.info("populating pathways")

        for reactome_id, (name, species) in tqdm(pathways_dict.items(), desc='Loading pathways'):

            if reactome_id in rid_pathway:
                pathway = rid_pathway[reactome_id]

            else:
                pathway = Pathway(
                    reactome_id=reactome_id,
                    name=name,
                )

                rid_pathway[reactome_id] = pathway
                self.session.add(pathway)

            pathway.species.append(species_name_to_model[species])

        self.session.commit()

    def _pathway_hierarchy(self, url=None):
        """ Links pathway models through hierarchy

        :param url: path or link to data source needed for get_data()
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

    def _pathway_protein(self, url=None):
        """ Populates UniProt Tables"""

        log.info("downloading proteins")

        uniprot_df = get_proteins_pathways_df(url=url)
        uniprots = parse_entities_pathways(uniprot_df)

        log.info("populating proteins")
        pid_protein = {}
        missing_reactome_ids = set()

        for uniprot_id, reactome_id, evidence in tqdm(uniprots, desc='Loading proteins'):
            if uniprot_id is None:
                log.warning('uniprot id is None')
                continue

            if uniprot_id in pid_protein:
                protein = pid_protein[uniprot_id]
            else:
                protein = Protein(uniprot_id=uniprot_id)
                pid_protein[uniprot_id] = protein
                self.session.add(protein)

            pathway = self.get_pathway_by_id(reactome_id)

            if pathway is None:
                log.debug('Missing reactome_id: %s', reactome_id)
                missing_reactome_ids.add(reactome_id)
                continue

            protein.pathways.append(pathway)

        if missing_reactome_ids:
            log.warning('missing %d reactome ids', len(missing_reactome_ids))

        self.session.commit()

    def _pathway_chemical(self, url=None):
        """ Populates Chebi Tables"""

        log.info("downloading chemicals")

        chebi_df = get_chemicals_pathways_df(url=url)
        chebis = parse_entities_pathways(chebi_df)

        log.info("populating chemicals")
        cid_chemical = {}
        missing_reactome_ids = set()

        for chebi_id, reactome_id, evidence in tqdm(chebis, desc='Loading chemicals'):
            if chebi_id is None:
                log.warning('chebi id is None')
                continue

            if chebi_id in cid_chemical:
                chemical = cid_chemical[chebi_id]
            else:
                chemical = Chemical(chebi_id=chebi_id)
                cid_chemical[chebi_id] = chemical
                self.session.add(chemical)

            pathway = self.get_pathway_by_id(reactome_id)

            if pathway is None:
                log.debug('Missing reactome_id: %s', reactome_id)
                missing_reactome_ids.add(reactome_id)
                continue

            chemical.pathways.append(pathway)

        if missing_reactome_ids:
            log.warning('missing %d reactome ids', len(missing_reactome_ids))

        self.session.commit()

    def populate(self, pathways_path=None, pathways_hierarchy_path=None, pathways_proteins_path=None,
                 pathways_chemicals_path=None):
        """ Populates all tables"""
        self._populate_pathways(url=pathways_path)
        self._pathway_hierarchy(url=pathways_hierarchy_path)
        self._pathway_protein(url=pathways_proteins_path)
        self._pathway_chemical(url=pathways_chemicals_path)
