# -*- coding: utf-8 -*-

import logging
from typing import Dict

from bel_resources import write_namespace

from pybel.constants import NAMESPACE_DOMAIN_BIOPROCESS
from .constants import PATHWAY_NAMES_URL
from .parsers.pathway_names import get_pathway_names_df

logger = logging.getLogger(__name__)

MODULE_NAME = 'reactome'


def get_values(url=None) -> Dict[str, str]:
    """Get the unique names from Reactome pathway names table. Combines all species.

    :param Optional[str] url: A non-default URL for the Reactome pathway names table
    """
    df = get_pathway_names_df(url=url)

    values = set(df[1])

    return {
        value: "B"
        for value in values
    }


def write_belns(file=None, url=None):
    """Print the Reactome Pathway names BEL namespace.

    :param file file: A writable file or file-like. Defaults to standard out
    """
    values = get_values(url=url)

    write_namespace(
        values=values,
        namespace_name="Reactome Pathway Names",
        namespace_keyword="REACTOME",
        namespace_domain=NAMESPACE_DOMAIN_BIOPROCESS,
        author_name='Charles Tapley Hoyt',
        citation_name=PATHWAY_NAMES_URL,
        namespace_species='9606',
        namespace_description="Reactome Pathways",
        author_copyright='Creative Commons by 4.0',
        author_contact="charles.hoyt@scai.fraunhofer.de",
        file=file
    )
