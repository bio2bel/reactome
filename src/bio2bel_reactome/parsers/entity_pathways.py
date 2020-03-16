# -*- coding: utf-8 -*-

"""This module parsers different molecular entities to pathways.

General file structure:

Column 1) UniProt, ChEBI identifier
Column 2) Reactome Stable identifier
Column 3) URL
Column 4) Event (Pathway or Reaction) Name
Column 5) Evidence Code [IEA, inferred by electronic annotation]
Column 6) Species

Column 4 and 6 are redundant since Reactome ID contains all info relative to species and event name
"""

import logging

import pandas as pd
from protmapper.api import hgnc_name_to_id
from protmapper.uniprot_client import get_hgnc_id, get_mnemonic

from bio2bel.downloading import make_df_getter
from pyobo import get_id_name_mapping, get_name_id_mapping
from ..constants import (
    CHEBI_PATHWAYS_PATH, CHEBI_PATHWAYS_URL, SPECIES_REMAPPING, UNIPROT_PATHWAYS_PATH, UNIPROT_PATHWAYS_URL,
)

__all__ = [
    'get_chemicals_pathways_df',
    'get_proteins_pathways_df',
    'get_procesed_proteins_pathways_df',
    'get_procesed_chemical_pathways_df',
]

logger = logging.getLogger(__name__)

get_proteins_pathways_df = make_df_getter(
    UNIPROT_PATHWAYS_URL,
    UNIPROT_PATHWAYS_PATH,
    sep='\t',
    header=None,
    names=['uniprot_id', 'reactome_id', 'reactome_link', 'reactome_name', 'evidence', 'species'],
)

chebi_id_to_name = get_id_name_mapping('chebi')
hgnc_id_to_name = {v: k for k, v in hgnc_name_to_id.items()}
species_name_to_id = get_name_id_mapping('ncbitaxon')


def get_procesed_proteins_pathways_df(*args, **kwargs) -> pd.DataFrame:
    """Get preprocessed proteins dataframe."""
    df = get_proteins_pathways_df(*args, **kwargs)
    del df['reactome_link']
    del df['reactome_name']
    del df['evidence']

    df['uniprot_accession'] = df['uniprot_id'].map(get_mnemonic)
    df['hgnc_id'] = df['uniprot_id'].map(get_hgnc_id)
    df['hgnc_symbol'] = df['hgnc_id'].map(hgnc_id_to_name.get)

    df['species'] = df['species'].map(lambda x: SPECIES_REMAPPING.get(x, x))
    df['species_taxonomy_id'] = df['species'].map(species_name_to_id.get)
    return df


get_chemicals_pathways_df = make_df_getter(
    CHEBI_PATHWAYS_URL,
    CHEBI_PATHWAYS_PATH,
    sep='\t',
    header=None,
    names=['chebi_id', 'reactome_id', 'reactome_link', 'reactome_name', 'evidence', 'species'],
    dtype={'chebi_id': str},
)


def get_procesed_chemical_pathways_df(*args, **kwargs) -> pd.DataFrame:
    """Get preprocessed chemicals dataframe."""
    df = get_chemicals_pathways_df(*args, **kwargs)
    del df['reactome_link']
    del df['reactome_name']
    del df['evidence']

    df['chebi_name'] = df['chebi_id'].map(chebi_id_to_name.get)

    df['species'] = df['species'].map(lambda x: SPECIES_REMAPPING.get(x, x))
    df['species_taxonomy_id'] = df['species'].map(species_name_to_id.get)
    return df
