# -*- coding: utf-8 -*-

import logging
import os

import click
from bio2bel.manager.compath import dict_to_df

from .manager import Manager

logger = logging.getLogger(__name__)

main = Manager.get_cli()


@main.command()
@click.option('-c', '--connection')
@click.option('-species', '--species', help="Specific species ex: --species='Homo sapiens'")
@click.option('-hierarchy', '--top-hierarchy', is_flag=True, help="Extract only the highest level in the hierarchy")
def export(connection, species, top_hierarchy):
    """Export all pathway - gene info to a excel file"""
    manager = Manager(connection=connection)

    logger.info("Querying the database")
    genesets = dict_to_df(manager.get_pathway_name_to_symbols(species=species, top_hierarchy=top_hierarchy))

    logger.info("Geneset exported to '{}/reactome_gene_sets.xlsx'".format(os.getcwd()))
    genesets.to_excel('reactome_gene_sets.xlsx', index=False)


if __name__ == '__main__':
    main()
