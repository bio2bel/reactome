# -*- coding: utf-8 -*-

""" This module contains the flask-admin application to visualize the db"""

import logging
import time

import flask_admin
from flask import Flask
from flask_bootstrap import Bootstrap

from bio2bel_reactome.manager import Manager
from bio2bel_reactome.models import *

log = logging.getLogger(__name__)

bootstrap = Bootstrap()


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
    :rtype: flask.Flask
    """

    t = time.time()

    app = Flask(__name__)
    bootstrap.init_app(app)

    manager = Manager(connection=connection)
    add_admin(app, manager.session, url=url)

    log.info('Done building %s in %.2f seconds', app, time.time() - t)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
