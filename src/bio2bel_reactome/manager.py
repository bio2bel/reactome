# -*- coding: utf-8 -*-

"""
This module populates the tables of bio2bel_reactome
"""

import configparser
import logging

from bio2bel_reactome.constants import *
from bio2bel_reactome.models import Base, Chemical, Pathway, Protein, Species
from bio2bel_reactome.parsers import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

    def _populate_pathways(self, source=None):
        """ Populate pathway table

        :param source: path or link to data source needed for get_data()
        """
        df = get_pathway_names_df(url=source)
        pathways_dict, species_set = parse_pathway_names(df)

        species_name_to_model = {}

        for species_name in species_set:
            new_species = Species(
                name=species_name,
            )

            self.session.add(new_species)
            species_name_to_model[species_name] = new_species

        for id, (name, species) in pathways_dict.items():
            new_pathway = Pathway(
                reactome_id=id,
                name=name,
                species=[species_name_to_model[species]]
            )

            self.session.add(new_pathway)

        self.session.commit()

    def _pathway_hierarchy(self, source=None):
        """ Links pathway models through hierarchy

        :param source: path or link to data source needed for get_data()
        """
        df = get_pathway_hierarchy_df(url=source)
        pathways_hierarchy = parse_pathway_hierarchy(df)

        for parent_id, child_id in pathways_hierarchy:
            parent = self.get_pathway_by_id(parent_id)
            child = self.get_pathway_by_id(child_id)

            parent.children.append(child)

        self.session.commit()

    def _pathway_entity(self, chebi_url=None, uniprot_url=None):
        """ Populates UniProt and Chebi Tables"""
        uniprot_df = get_proteins_pathways_df(url=uniprot_url)
        uniprots = parse_entities_pathways(uniprot_df)

        pid_protein = {}
        cid_chemical = {}

        for uniprot_id, reactome_id, evidence in uniprots:
            if uniprot_id in pid_protein:
                protein = pid_protein[uniprot_id]
            else:
                protein = Protein(uniprot_id=uniprot_id)
                pid_protein[uniprot_id] = protein
                self.session.add(protein)

            pathway = self.get_pathway_by_id(reactome_id)
            protein.pathways.append(pathway)

        chebi_df = get_chemicals_pathways_df(url=chebi_url)
        chebis = parse_entities_pathways(chebi_df)

        for chebi_id, reactome_id, evidence in chebis:

            if chebi_id in cid_chemical:
                chemical = cid_chemical[chebi_id]
            else:
                chemical = Chemical(chebi_id=chebi_id)
                cid_chemical[chebi_id] = chemical
                self.session.add(chemical)

            pathway = self.get_pathway_by_id(reactome_id)
            chemical.pathways.append(pathway)

    def populate(self):
        """ Populates all tables"""
        self._populate_pathways()
        self._pathway_hierarchy()
