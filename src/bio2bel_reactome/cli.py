# -*- coding: utf-8 -*-

import logging
import os

import click

from .manager import Manager
from .utils import dict_to_pandas_df

log = logging.getLogger(__name__)

main = Manager.get_cli()


@main.command()
@click.option('-c', '--connection')
@click.option('-species', '--species', help="Specific species ex: --species='Homo sapiens'")
@click.option('-hierarchy', '--top-hierarchy', is_flag=True, help="Extract only the highest level in the hierarchy")
def export(connection, species, top_hierarchy):
    """Export all pathway - gene info to a excel file"""
    m = Manager(connection=connection)

    log.info("Querying the database")

    genesets = dict_to_pandas_df(m.export_gene_sets(species=species, top_hierarchy=top_hierarchy))

    log.info("Geneset exported to '{}/reactome_gene_sets.xlsx'".format(os.getcwd()))

    genesets.to_excel('reactome_gene_sets.xlsx', index=False)


if __name__ == '__main__':
    main()
