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
import logging
from bio2bel_reactome.constants import CHEBI_PATHWAYS_URL, UNIPROT_PATHWAYS_URL

__all__ = [
    'get_chemicals_pathways_df',
    'get_proteins_pathways_df',
    'parse_entities_pathways',
    'get_hgnc_symbol_id_by_uniprot_id',
]

log = logging.getLogger(__name__)


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


def parse_entities_pathways(entities_pathways_df, only_human=True):
    """ Parser the entity - pathway dataframe

    :param pandas.DataFrame entities_pathways_df: File as dataframe
    :param bool only_human: parse only human entities. Defaults to True.
    :rtype: list[tuple]
    :return Object representation dictionary (entity_id, reactome_id, evidence)
    """
    if only_human:
        log.info('only importing human pathways')

        return [
            (row[0], row[1], row[4])
            for _, row in entities_pathways_df.iterrows()
            if row[5] == 'Homo sapiens'
        ]

    return [
        (row[0], row[1], row[4])
        for _, row in entities_pathways_df.iterrows()
    ]


def get_hgnc_symbol_id_by_uniprot_id(hgnc_manager, uniprot_id):
    """Returns HGNC symbol and id from PyHGNC query

    :param bio2bel_hgnc.Manager hgnc_manager: Manager
    :param str uniprot_id: UniProt identifier
    :rtype: Optional[pyhgnc.models.HGNC]
    """
    gene = hgnc_manager.hgnc(uniprotid=uniprot_id)

    if not gene:

        # Checks if minus is part of the uniprot id -> isoform signature
        if '-' not in uniprot_id:
            return None

        isoform_uniprot_id = uniprot_id.split('-')[0]

        gene = hgnc_manager.hgnc(uniprotid=isoform_uniprot_id)

        if not gene:
            return None

    return gene
