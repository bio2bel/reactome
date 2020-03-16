# -*- coding: utf-8 -*-

"""This module contains all the constants used in bio2bel Reactome project."""

import os

from bio2bel.utils import get_data_dir
from pyobo.path_utils import get_url_filename

MODULE_NAME = 'reactome'
DATA_DIR = get_data_dir(MODULE_NAME)

PATHWAY_NAMES_URL = 'https://reactome.org/download/current/ReactomePathways.txt'
PATHWAY_NAMES_PATH = os.path.join(DATA_DIR, get_url_filename(PATHWAY_NAMES_URL))

PATHWAYS_HIERARCHY_URL = 'https://reactome.org/download/current/ReactomePathwaysRelation.txt'
PATHWAYS_HIERARCHY_PATH = os.path.join(DATA_DIR, get_url_filename(PATHWAYS_HIERARCHY_URL))

UNIPROT_PATHWAYS_URL = 'https://reactome.org/download/current/UniProt2Reactome_All_Levels.txt'
UNIPROT_PATHWAYS_PATH = os.path.join(DATA_DIR, get_url_filename(UNIPROT_PATHWAYS_URL))

CHEBI_PATHWAYS_URL = 'https://reactome.org/download/current/ChEBI2Reactome_All_Levels.txt'
CHEBI_PATHWAYS_PATH = os.path.join(DATA_DIR, get_url_filename(CHEBI_PATHWAYS_URL))

# Namespace constants
REACTOME = 'reactome'
HGNC = 'hgnc'
UNIPROT = 'uniprot'
CHEBI = 'chebi'

SPECIES_REMAPPING = {
    'Canis familiaris': 'Canis lupus familiaris',
}
