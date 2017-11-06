# -*- coding: utf-8 -*-

"""
This module parsers different molecular entities to pathways

General file structure:

Column 1) UniProt, Chebi identifier
Column 2) Reactome Stable identifier
Column 3) URL
Column 4) Event (Pathway or Reaction) Name
Column 5) Evidence Code [IEA, inferred by electronic annotation]
Column 6) Species

Column 4 and 6 are redundant since Reactome ID contains all info relative to species and event name
"""

import pandas as pd

from bio2bel_reactome.constants import CHEBI_PATHWAYS_URL, UNIPROT_PATHWAYS_URL

__all__ = [
    'get_chemicals_pathways_df',
    'get_proteins_pathways_df',
    'parse_entities_pathways',
]


def _get_data_helper(default_url, url=None):
    """

    :param str default_url:
    :param Optional[str] url:
    :rtype: pandas.DataFrame
    """
    return pd.read_csv(
        url or default_url,
        sep='\t',
        header=None
    )


def get_proteins_pathways_df(url=None):
    """Gets the protein to pathways mapping

    :param Optional[str] url:
    :rtype: pandas.DataFrame
    """
    return _get_data_helper(UNIPROT_PATHWAYS_URL, url=url)


def get_chemicals_pathways_df(url=None):
    """Gets the chemicals to pathways mapping

    :param Optional[str] url:
    :rtype: pandas.DataFrame
    """
    return _get_data_helper(CHEBI_PATHWAYS_URL, url=url)


def parse_entities_pathways(entities_pathways_df):
    """ Parser the entity - pathway dataframe

    :param pandas.DataFrame entities_pathways_df: File as dataframe
    :rtype: list[tuple]
    :return Object representation dictionary (entity_id, reactome_id, evidence)
    """
    return [
        (row[0], row[1], row[4])
        for _, row in entities_pathways_df.iterrows()
    ]
