# -*- coding: utf-8 -*-

from __future__ import print_function

import logging

from bio2bel_reactome.constants import PATHWAY_NAMES_URL
from bio2bel_reactome.parsers.pathway_names import get_pathway_names_df
from pybel.constants import NAMESPACE_DOMAIN_BIOPROCESS
from pybel.resources.arty import get_today_arty_namespace
from pybel.resources.definitions import write_namespace
from pybel.resources.deploy import deploy_namespace


log = logging.getLogger(__name__)

MODULE_NAME = 'reactome'


def get_values(url=None):
    """Gets the unique names from Reactome pathway names table. Combines all species.

    :param Optional[str] url: A non-default URL for the Reactome pathway names table
    :rtype: set[str]
    """
    df = get_pathway_names_df(url=url)

    values = set(df[1])

    return values


def write_belns(file=None, url=None):
    """Prints the Reactome Pathway names BEL namespace

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


def deploy_to_arty(quit_fail_redeploy=True):
    """Gets the data, writes BEL namespace, and writes BEL knowledge to Artifactory"""

    file_name = get_today_arty_namespace(MODULE_NAME)

    with open(file_name, 'w') as file:
        write_belns(file)

    namespace_deploy_success = deploy_namespace(file_name, MODULE_NAME)

    if not namespace_deploy_success and quit_fail_redeploy:
        log.warning('did not redeploy')
        return False
