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


def parser_entity_pathways(entity_pathway_dataframe):
    """ Parser the entity - pathway dataframe

    :param pandas.DataFrame pathway_dataframe: File as dataframe
    :rtype tuple
    :return Object representation dictionary (entity_id, reactome_id, evidence)
    """

    entity_pathway_table = [
        (row[0], row[1], row[4])
        for _, row in entity_pathway_dataframe.iterrows()
    ]

    return entity_pathway_table
