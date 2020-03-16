# -*- coding: utf-8 -*-

"""This module parsers the Reactome pathway names file.

The "Complete list of pathways" file maps the Reactome Stable identifier (ST_ID) to a pathway name and corresponding species.
"""

import pandas as pd

from bio2bel.downloading import make_df_getter
from bio2bel_reactome.constants import PATHWAY_NAMES_PATH, PATHWAY_NAMES_URL

__all__ = [
    'get_pathway_names_df',
    'parse_pathway_names',
]

get_pathway_names_df = make_df_getter(
    PATHWAY_NAMES_URL,
    PATHWAY_NAMES_PATH,
    sep='\t',
    header=None,
)


def parse_pathway_names(pathway_names_df: pd.DataFrame):
    """Parse the pathway name dataframe.

    :param pathway_names_df: Pathway hierarchy as dataframe
    :rtype: dict
    :return Object representation dictionary (reactome_id: (name, species))
    :rtype: set
    :return all species names
    """
    pathways = {}
    species_set = set()

    for reactome_id, name, species in pathway_names_df.values:
        pathways[reactome_id] = (name.strip(), species)
        species_set.add(species)

    return pathways, species_set
