# -*- coding: utf-8 -*-

"""
This module parsers the Reactome pathway names file

The "Complete list of pathways" file maps the Reactome Stable identifier (ST_ID) to a pathway name and corresponding species.
"""

import pandas as pd

from bio2bel_reactome.constants import PATHWAY_NAMES_URL

__all__ = [
    'get_pathway_names_df',
    'parse_pathway_names',
]


def get_pathway_names_df(url=None):
    """ Converts tab separated txt files to pandas Dataframe

    :param Optional[str] url: url from reactome tab separated file
    :return: dataframe of the file
    :rtype: pandas.DataFrame
    """
    df = pd.read_csv(
        url or PATHWAY_NAMES_URL,
        sep='\t',
        header=None
    )
    return df


def parse_pathway_names(pathway_names_df):
    """ Parser the pathway name dataframe

    :param pandas.DataFrame pathway_names_df: Pathway hierarchy as dataframe
    :rtype: dict
    :return Object representation dictionary (reactome_id: (name, species))
    :rtype: set
    :return all species names
    """

    pathways = {}
    species_set = set()

    for _, (reactome_id, name, species) in pathway_names_df.iterrows():
        pathways[reactome_id] = (name, species)
        species_set.add(species)

    return pathways, species_set
