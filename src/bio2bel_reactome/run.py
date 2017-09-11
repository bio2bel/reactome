# -*- coding: utf-8 -*-

from __future__ import print_function

import pandas as pd
from pybel.constants import NAMESPACE_DOMAIN_BIOPROCESS
from pybel_tools.definition_utils import write_namespace

from bio2bel_reactome.constants import names_url


def get_data():
    """Gets the names list from Reactome. Includes 3 columns - ID's, names, and species

    :rtype: pandas.DataFrame
    """
    df = pd.read_csv(names_url, sep='\t', header=None)
    return df


def get_values(df=None):
    """Gets the unique names from Reactome pathway names table. Combines all species.

    :rtype: set[str]
    """
    if df is None:
        df = get_data()

    values = set(df[1])

    return values


def write_belns(file=None):
    """Prints the Reactome Pathway names BEL namespace

    :param file file: A writable file or file-like. Defaults to standard out
    """
    values = get_values()

    write_namespace(
        namespace_name="Reactome Pathway Names",
        namespace_keyword="REACTOME",
        namespace_domain=NAMESPACE_DOMAIN_BIOPROCESS,
        author_name='Charles Tapley Hoyt',
        citation_name=names_url,
        values=values,
        namespace_species='9606',
        namespace_description="Reactome Pathways",
        author_copyright='Creative Commons by 4.0',
        functions="B",
        author_contact="charles.hoyt@scai.fraunhofer.de",
        file=file
    )
