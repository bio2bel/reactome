# -*- coding: utf-8 -*-

""" This module contains the flask-admin application to visualize the db"""

import logging
import time

import flask_admin
from flask import Flask
from flask_admin.contrib.sqla import ModelView

from .manager import Manager
from .models import *

log = logging.getLogger(__name__)


class PathwayView(ModelView):
    """Pathway view in Flask-admin"""
    column_searchable_list = (
        Pathway.reactome_id,
        Pathway.name,
    )


class ProteinView(ModelView):
    """Protein view in Flask-admin"""
    column_searchable_list = (
        Protein.hgnc_symbol,
        Protein.uniprot_id,
        Protein.hgnc_id
    )


class SpeciesView(ModelView):
    """Species view in Flask-admin"""
    column_searchable_list = (
        Species.name,
    )


class ChemicalView(ModelView):
    """Chemical view in Flask-admin"""
    column_searchable_list = (
        Chemical.chebi_id,
    )


def add_admin(app, session, **kwargs):
    admin = flask_admin.Admin(app, **kwargs)
    admin.add_view(PathwayView(Pathway, session))
    admin.add_view(ProteinView(Protein, session))
    admin.add_view(ChemicalView(Chemical, session))
    admin.add_view(SpeciesView(Species, session))
    return admin


def create_app(connection=None, url=None):
    """Creates a Flask application

    :type connection: Optional[str]
    :type url: Optional[str]
    :rtype: flask.Flask
    """
    t = time.time()

    app = Flask(__name__)

    manager = Manager.ensure(connection=connection)
    add_admin(app, manager.session, url=url)

    log.info('Done building %s in %.2f seconds', app, time.time() - t)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
