# -*- coding: utf-8 -*-

""" This module contains the common views across all pathway bio2bel repos"""

import logging

from flask import Blueprint, render_template, send_file

from bio2bel_reactome.manager import Manager
from bio2bel_reactome.utils import dict_to_pandas_df

log = logging.getLogger(__name__)

ui_blueprint = Blueprint('ui', __name__)


@ui_blueprint.route('/', methods=['GET', 'POST'])
def home():
    """ComPathTool home page
    """
    return render_template('home.html')


@ui_blueprint.route('/imprint', methods=['GET', 'POST'])
def imprint():
    """Imprint page
    """
    return render_template('imprint.html')


@ui_blueprint.route('/about', methods=['GET', 'POST'])
def about():
    """About page
    """
    return render_template('about.html')


@ui_blueprint.route('/export_genesets', methods=['GET', 'POST'])
def export_genesets():
    """Export genesets page
    """

    m = Manager()

    log.info("Querying the database")

    genesets = dict_to_pandas_df(m.export_genesets())

    return send_file(
        genesets.to_csv('genesets.csv', index=False),
        mimetype='text/csv',
        attachment_filename='genesets.csv',
        as_attachment=True
    )
