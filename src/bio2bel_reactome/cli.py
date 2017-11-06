# -*- coding: utf-8 -*-

from __future__ import print_function

import logging

import click

from bio2bel_reactome.manager import Manager
from bio2bel_reactome.to_belns import deploy_to_arty

log = logging.getLogger('pyreactome')


def set_debug(level):
    logging.basicConfig(level=level, format="%(asctime)s - %(levelname)s - %(message)s")


def set_debug_param(debug):
    if debug == 1:
        set_debug(20)
    elif debug == 2:
        set_debug(10)


@click.group()
def main():
    """Reactome to BEL"""
    logging.basicConfig(level=10, format="%(asctime)s - %(levelname)s - %(message)s")


@main.command()
@click.option('-v', '--debug', count=True, help="Turn on debugging.")
def build(debug):
    """Build the local version of the full Reactome."""

    set_debug_param(debug)

    m = Manager()
    click.echo("populate tables")
    m.populate()


@main.command()
@click.option('-v', '--debug', count=True, help="Turn on debugging.")
def drop(debug):
    """Drop the Reactome database."""

    set_debug_param(debug)

    m = Manager()
    click.echo("drop db")
    m.drop_tables()


@main.command()
@click.option('--force', is_flag=True, help="Force knowledge to be uploaded even if not new namespace")
def deploy(force):
    """Deploy to Artifactory"""
    deploy_to_arty(not force)


if __name__ == '__main__':
    main()
