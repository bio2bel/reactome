# -*- coding: utf-8 -*-

"""This module contains all the constants used in bio2bel Reactome project"""

import os

from bio2bel.utils import get_data_dir

MODULE_NAME = 'reactome'
DATA_DIR = get_data_dir(MODULE_NAME)

PATHWAY_NAMES_URL = 'https://reactome.org/download/current/ReactomePathways.txt'
PATHWAY_NAMES_PATH = os.path.join(DATA_DIR, PATHWAY_NAMES_URL.split('/')[-1])

PATHWAYS_HIERARCHY_URL = 'https://reactome.org/download/current/ReactomePathwaysRelation.txt'
PATHWAYS_HIERARCHY_PATH = os.path.join(DATA_DIR, PATHWAYS_HIERARCHY_URL.split('/')[-1])

UNIPROT_PATHWAYS_URL = 'https://reactome.org/download/current/UniProt2Reactome_All_Levels.txt'
UNIPROT_PATHWAYS_PATH = os.path.join(DATA_DIR, UNIPROT_PATHWAYS_URL.split('/')[-1])

CHEBI_PATHWAYS_URL = 'https://reactome.org/download/current/ChEBI2Reactome_All_Levels.txt'
CHEBI_PATHWAYS_PATH = os.path.join(DATA_DIR, CHEBI_PATHWAYS_URL.split('/')[-1])

REACTOME_PATHWAY_LINK = 'https://reactome.org/PathwayBrowser/'

# Namespace constants
REACTOME = 'reactome'
HGNC = 'hgnc'
UNIPROT = 'uniprot'
CHEBI = 'chebi'
