# -*- coding: utf-8 -*-

"""
This module parsers the Reactome pathway hierarchy tab-separated table

"Pathway hierarchy relationship" file consists of two columns of Reactome Stable identifiers (ST_ID),
defining the relationship between pathways within the pathway hierarchy.
The first column provides the parent pathway stable identifier, whereas the second column provides the
child pathway stable identifier.
"""

import pandas as pd

from bio2bel_reactome.constants import PATHWAYS_HIERARCHY_URL

__all__ = [
    'get_pathway_hierarchy_df',
    'parse_pathway_hierarchy',
]

def get_pathway_hierarchy_df(url=None):
    """ Converts tab separated txt files to pandas Dataframe

    :param Optional[str] url: url from reactome tab separated file
    :return: dataframe of the file
    :rtype: pandas.DataFrame
    """
    df = pd.read_csv(
        url or PATHWAYS_HIERARCHY_URL,
        sep='\t',
        header=None
    )

    return df


def parse_pathway_hierarchy(pathway_dataframe):
    """ Parser the pathway hierarchy dataframe

    :param pandas.DataFrame pathway_dataframe: Parent - child pathway relationships
    :rtype: list[tuple]
    :return Relationship representation (reactome_parent_id, reactome_child_id)
    """
    return [
        (row[0], row[1])
        for _, row in pathway_dataframe.iterrows()
    ]
