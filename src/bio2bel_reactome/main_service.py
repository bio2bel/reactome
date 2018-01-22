# -*- coding: utf-8 -*-

""" This module contains the common views across all pathway bio2bel repos"""

import logging

from flask import Blueprint, render_template

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
