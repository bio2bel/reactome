# -*- coding: utf-8 -*-

from __future__ import print_function

import logging

import click

from bio2bel_reactome.constants import DEFAULT_CACHE_CONNECTION
from bio2bel_reactome.manager import Manager
from bio2bel_reactome.to_belns import deploy_to_arty

log = logging.getLogger(__name__)


def set_debug(level):
    logging.basicConfig(level=level, format="%(asctime)s - %(levelname)s - %(message)s")
    log.setLevel(level=level)


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
@click.option('-c', '--connection', help='Defaults to {}'.format(DEFAULT_CACHE_CONNECTION))
def populate(connection):
    """Build the local version of the full Reactome."""
    m = Manager(connection=connection)
    m.populate()


@main.command()
@click.option('-c', '--connection', help='Defaults to {}'.format(DEFAULT_CACHE_CONNECTION))
def drop(connection):
    """Drop the Reactome database."""
    m = Manager(connection=connection)
    m.drop_all()


@main.command()
@click.option('--force', is_flag=True, help="Force knowledge to be uploaded even if not new namespace")
def deploy(force):
    """Deploy to Artifactory"""
    deploy_to_arty(not force)


@main.command()
def web():
    """Run web"""
    from bio2bel_reactome.web import app
    app.run(debug=True, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
