# -*- coding: utf-8 -*-

import logging

from bio2bel_reactome.constants import PATHWAY_NAMES_URL
from bio2bel_reactome.parsers.pathway_names import get_pathway_names_df
from pybel.constants import NAMESPACE_DOMAIN_BIOPROCESS
from pybel.resources.definitions import write_namespace

log = logging.getLogger(__name__)

MODULE_NAME = 'reactome'


def get_values(url=None):
    """Get the unique names from Reactome pathway names table. Combines all species.

    :param Optional[str] url: A non-default URL for the Reactome pathway names table
    :rtype: set[str]
    """
    df = get_pathway_names_df(url=url)

    values = set(df[1])

    return values


def write_belns(file=None, url=None):
    """Print the Reactome Pathway names BEL namespace.

    :param file file: A writable file or file-like. Defaults to standard out
    """
    values = get_values(url=url)

    write_namespace(
        namespace_name="Reactome Pathway Names",
        namespace_keyword="REACTOME",
        namespace_domain=NAMESPACE_DOMAIN_BIOPROCESS,
        author_name='Charles Tapley Hoyt',
        citation_name=PATHWAY_NAMES_URL,
        values=values,
        namespace_species='9606',
        namespace_description="Reactome Pathways",
        author_copyright='Creative Commons by 4.0',
        functions="B",
        author_contact="charles.hoyt@scai.fraunhofer.de",
        file=file
    )
