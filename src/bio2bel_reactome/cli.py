# -*- coding: utf-8 -*-

from __future__ import print_function

import logging
import os
import sys

import click
from pybel_tools.ols_utils import OlsNamespaceOntology

from .constants import DEFAULT_CACHE_CONNECTION, MODULE_DOMAIN, MODULE_FUNCTION, MODULE_NAME
from .manager import Manager
from .to_belns import deploy_to_arty
from .utils import dict_to_pandas_df

log = logging.getLogger(__name__)


def set_debug(level):
    logging.basicConfig(level=level, format="%(asctime)s - %(levelname)s - %(message)s")
    log.setLevel(level=level)


def set_debug_param(debug):
    if debug == 0:
        set_debug(30)
    elif debug == 1:
        set_debug(20)
    elif debug == 2:
        set_debug(10)


@click.group(help='Convert Reactome to BEL. Default connection at {}'.format(DEFAULT_CACHE_CONNECTION))
def main():
    pass


@main.command()
@click.option('-v', '--debug', count=True, help="Turn on debugging.")
@click.option('-c', '--connection', help="Defaults to {}".format(DEFAULT_CACHE_CONNECTION))
@click.option('-d', '--reset-db', default=True)
@click.option('-n', '--not-only-human', is_flag=True, help="Do not only build with human")
def populate(debug, connection, reset_db, not_only_human):
    """Build the local version of Reactome."""

    set_debug_param(debug)

    m = Manager(connection=connection)

    if reset_db is True:
        log.info('Deleting the previous instance of the database')
        m.drop_all()
        log.info('Creating new models')
        m.create_all()

    m.populate(only_human=(not not_only_human))


@main.command()
@click.option('-v', '--debug', count=True, help="Turn on debugging.")
@click.option('-y', '--yes', is_flag=True)
@click.option('-c', '--connection', help='Defaults to {}'.format(DEFAULT_CACHE_CONNECTION))
def drop(debug, yes, connection):
    """Drop the Reactome database."""

    set_debug_param(debug)

    if yes or click.confirm('Do you really want to delete the database?'):
        m = Manager(connection=connection)
        click.echo("drop db")
        m.drop_all()


@main.command()
@click.option('--force', is_flag=True, help="Force knowledge to be uploaded even if not new namespace")
def deploy(force):
    """Deploy to Artifactory"""
    deploy_to_arty(not force)


@main.command()
@click.option('-b', '--ols-base', help="Custom OLS base url")
@click.option('-o', '--output', type=click.File('w'), default=sys.stdout)
def write(ols_base, output):
    """Writes BEL namespace"""
    ontology = OlsNamespaceOntology(MODULE_NAME, MODULE_DOMAIN, bel_function=MODULE_FUNCTION, ols_base=ols_base)
    ontology.write_namespace(output)


@main.command()
@click.option('-c', '--connection', help="Defaults to {}".format(DEFAULT_CACHE_CONNECTION))
@click.option('-species', '--species', help="Specific species ex: --species='Homo sapiens'")
@click.option('-hierarchy', '--top-hierarchy', is_flag=True, help="Extract only the highest level in the hierarchy")
def export(connection, species, top_hierarchy):
    """Export all pathway - gene info to a excel file"""
    m = Manager(connection=connection)

    log.info("Querying the database")

    genesets = dict_to_pandas_df(m.export_genesets(species=species, top_hierarchy=top_hierarchy))

    log.info("Geneset exported to '{}/reactome_gene_sets.xlsx'".format(os.getcwd()))

    genesets.to_excel('reactome_gene_sets.xlsx', index=False)


@main.command()
@click.option('-v', '--debug', count=True, help="Turn on debugging.")
@click.option('-c', '--connection', help="Defaults to {}".format(DEFAULT_CACHE_CONNECTION))
@click.option('-p', '--port', type=int)
@click.option('-h', '--host')
def web(debug, connection, port, host):
    """Run web"""
    set_debug_param(debug)

    from bio2bel_reactome.web import create_app
    app = create_app(connection=connection)
    app.run(host=host, port=port)


if __name__ == '__main__':
    main()
