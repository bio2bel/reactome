# -*- coding: utf-8 -*-

"""This module contains all the constants used in bio2bel Reactome project"""

import os

REACTOME_DATA_DIR = os.path.join(os.path.expanduser('~'), '.reactome')

if not os.path.exists(REACTOME_DATA_DIR):
    os.makedirs(REACTOME_DATA_DIR)

REACTOME_DATABASE_NAME = 'reactome.db'
REACTOME_SQLITE_PATH = 'sqlite:///' + os.path.join(REACTOME_DATA_DIR, REACTOME_DATABASE_NAME)

REACTOME_CONFIG_FILE_PATH = os.path.join(REACTOME_DATA_DIR, 'config.ini')


PATHWAY_NAMES_URL = 'http://reactome.org/download/current/ReactomePathways.txt'
PATHWAYS_HIERARCHY_URL = 'http://reactome.org/download/current/ReactomePathwaysRelation.txt'
UNIPROT_PATHWAYS_URL = 'http://reactome.org/download/current/UniProt2Reactome_All_Levels.txt'
CHEBI_PATHWAYS_URL = 'http://reactome.org/download/current/ChEBI2Reactome_All_Levels.txt'

REACTOME_PATHWAY_LINK = 'http://reactome.org/PathwayBrowser/'
