# -*- coding: utf-8 -*-

"""
This module parsers the Reactome pathway names file

The "Complete list of pathways" file maps the Reactome Stable identifier (ST_ID) to a pathway name and corresponding species.

"""


def parser_pathway_names(pathway_dataframe):
    """ Parser the pathway name dataframe

    :param pandas.DataFrame pathway_dataframe: Pathway hierarchy as dataframe
    :rtype dict
    :return Object representation dictionary (reactome_id: (species, name))
    """

    pathways = {
        row[0]: (row[1], row[2])
        for _, row in pathway_dataframe.iterrows()
    }

    return pathways
