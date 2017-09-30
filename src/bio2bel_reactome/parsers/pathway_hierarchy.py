# -*- coding: utf-8 -*-

"""
This module parsers the Reactome pathway hierarchy tab-separated table

"Pathway hierarchy relationship" file consists of two columns of Reactome Stable identifiers (ST_ID),
defining the relationship between pathways within the pathway hierarchy.
The first column provides the parent pathway stable identifier, whereas the second column provides the
child pathway stable identifier.

"""

def parser_pathway_hierarchy(pathway_dataframe):
    """ Parser the pathway hierarchy dataframe

    :param pandas.DataFrame pathway_dataframe: Parent - child pathway relationships
    :rtype tuple
    :return Relationship representation (reactome_parent_id, reactome_child_id)
    """

    pathway_parent_to_child = [
        (row[0],row[1])
        for _, row in pathway_dataframe.iterrows()
    ]

    return pathway_parent_to_child