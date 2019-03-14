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
import os
from typing import List, Optional, Tuple

import pandas as pd

import bio2bel_hgnc
from bio2bel.downloading import make_df_getter
from bio2bel_hgnc.models import HumanGene
from bio2bel_reactome.constants import (
    CHEBI_PATHWAYS_PATH, CHEBI_PATHWAYS_URL, UNIPROT_PATHWAYS_PATH, UNIPROT_PATHWAYS_URL,
)

__all__ = [
    'get_chemicals_pathways_df',
    'get_proteins_pathways_df',
    'parse_entities_pathways',
    'get_hgnc_symbol_id_by_uniprot_id',
]

log = logging.getLogger(__name__)

get_proteins_pathways_df = make_df_getter(UNIPROT_PATHWAYS_URL, UNIPROT_PATHWAYS_PATH, sep='\t', header=None)
get_chemicals_pathways_df = make_df_getter(CHEBI_PATHWAYS_URL, CHEBI_PATHWAYS_PATH, sep='\t', header=None)


def parse_entities_pathways(entities_pathways_df: pd.DataFrame, only_human: bool = True) -> List[Tuple]:
    """Parse the entity - pathway dataframe.

    :param  entities_pathways_df: File as dataframe
    :param  only_human: parse only human entities. Defaults to True.
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


def get_hgnc_symbol_id_by_uniprot_id(hgnc_manager: bio2bel_hgnc.Manager, uniprot_id: str) -> Optional[HumanGene]:
    """Return HGNC symbol and id from a Bio2BEL query."""
    gene = hgnc_manager.hgnc(uniprotid=uniprot_id)

    if not gene:

        # Check if minus is part of the uniprot id -> isoform signature
        if '-' not in uniprot_id:
            return None

        isoform_uniprot_id = uniprot_id.split('-')[0]

        gene = hgnc_manager.hgnc(uniprotid=isoform_uniprot_id)

        if not gene:
            return None

    return gene
