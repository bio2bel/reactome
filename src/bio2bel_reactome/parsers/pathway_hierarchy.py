# -*- coding: utf-8 -*-

"""This module parsers the Reactome pathway hierarchy tab-separated table.

"Pathway hierarchy relationship" file consists of two columns of Reactome Stable identifiers (ST_ID),
defining the relationship between pathways within the pathway hierarchy.
The first column provides the parent pathway stable identifier, whereas the second column provides the
child pathway stable identifier.
"""

import pandas as pd
from bio2bel.downloading import make_df_getter

from ..constants import PATHWAYS_HIERARCHY_PATH, PATHWAYS_HIERARCHY_URL

__all__ = [
    'get_pathway_hierarchy_df',
    'parse_pathway_hierarchy',
]

get_pathway_hierarchy_df = make_df_getter(
    PATHWAYS_HIERARCHY_URL,
    PATHWAYS_HIERARCHY_PATH,
    sep='\t',
    header=None,
)


def parse_pathway_hierarchy(pathway_dataframe: pd.DataFrame):
    """Parse the pathway hierarchy dataframe.

    :param pathway_dataframe: Parent - child pathway relationships
    :rtype: list[tuple]
    :return Relationship representation (reactome_parent_id, reactome_child_id)
    """
    return [
        (row[0], row[1])
        for _, row in pathway_dataframe.iterrows()
    ]
