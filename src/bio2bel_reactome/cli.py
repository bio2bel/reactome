# -*- coding: utf-8 -*-

from __future__ import print_function

import logging
import sys

import click

from bio2bel_reactome.run import write_belns, deploy_to_arty


@click.group()
def main():
    """Reactome to BEL"""
    logging.basicConfig(level=10, format="%(asctime)s - %(levelname)s - %(message)s")


@main.command()
@click.option('-o', '--output', type=click.File('w'), default=sys.stdout)
def write(output):
    """Writes BEL namespace"""
    write_belns(output)


@main.command()
@click.option('--force', is_flag=True, help="Force knowledge to be uploaded even if not new namespace")
def deploy(force):
    """Deploy to Artifactory"""
    deploy_to_arty(not force)


if __name__ == '__main__':
    main()
