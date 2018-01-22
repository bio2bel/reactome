# -*- coding: utf-8 -*-

""" This module contains views specific to the Bio2BEL reactome package"""

import logging

from flask import Blueprint

log = logging.getLogger(__name__)

ui_blueprint = Blueprint('reactome', __name__)


@ui_blueprint.route('/reactome/export', methods=['GET', 'POST'])
def export_reactome():
    """Export Reactome gene sets to excel
    """
    NotImplemented
