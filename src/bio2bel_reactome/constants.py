# -*- coding: utf-8 -*-

"""This module contains all the constants used in bio2bel Reactome project"""

from bio2bel.utils import get_connection, get_data_dir

MODULE_NAME = 'reactome'
DATA_DIR = get_data_dir(MODULE_NAME)
DEFAULT_CACHE_CONNECTION = get_connection(MODULE_NAME)

PATHWAY_NAMES_URL = 'http://reactome.org/download/current/ReactomePathways.txt'
PATHWAYS_HIERARCHY_URL = 'http://reactome.org/download/current/ReactomePathwaysRelation.txt'
UNIPROT_PATHWAYS_URL = 'http://reactome.org/download/current/UniProt2Reactome_All_Levels.txt'
CHEBI_PATHWAYS_URL = 'http://reactome.org/download/current/ChEBI2Reactome_All_Levels.txt'

REACTOME_PATHWAY_LINK = 'http://reactome.org/PathwayBrowser/'

# Namespace constants

REACTOME = 'REACTOME'
HGNC = 'HGNC'
CHEBI = 'CHEBI'