# -*- coding: utf-8 -*-

"""
This module populates the UniProt Table and links it with the Pathway table
"""

import configparser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bio2bel_reactome.constants import *
from bio2bel_reactome.parsers.pathway_names import parser_pathway_names
from bio2bel_reactome.models import Base, Pathway
from bio2bel_reactome.run import get_data

import logging

log = logging.getLogger(__name__)


class Manager(object):
    def __init__(self, connection=None):
        self.connection = self.get_connection(connection)
        self.engine = create_engine(self.connection)
        self.sessionmake = sessionmaker(bind=self.engine, autoflush=False, expire_on_commit=False)
        self.session = self.sessionmake()
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
        Base.metadata.create_all(self.engine, checkfirst=check_first)

    @staticmethod
    def ensure(connection=None):
        """Checks and allows for a Manager to be passed to the function. """
        if connection is None or isinstance(connection, str):
            return Manager(connection=connection)

        if isinstance(connection, Manager):
            return connection

        raise TypeError

    """Custom Methods to Populate the DB"""

    def _populate_pathways(self, source=None):
        """ Populate pathway table

        :param source: path or link to data source needed for get_data()
        """

        if source is None:
            source = PATHWAY_NAMES_URL

        df = get_data(source)

        pathways_dict = parser_pathway_names(df)

        for id, (species, name) in pathways_dict.items():
            new_pathway = Pathway(
                reactome_id=id,
                pathway_name=species,
                pathway_species=name
            )

            self.session.add(new_pathway)

        self.session.commit()

    def populate(self, source=None):

        raise NotImplementedError
