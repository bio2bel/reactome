# -*- coding: utf-8 -*-

""" This module contains the flask application to visualize the db"""

import flask
import flask_admin
from bio2bel_reactome.manager import Manager
from bio2bel_reactome.models import *
from flask_admin.contrib.sqla import ModelView

app = flask.Flask(__name__)
admin = flask_admin.Admin(app)

manager = Manager()

admin.add_view(ModelView(Pathway, manager.session))
admin.add_view(ModelView(Protein, manager.session))
admin.add_view(ModelView(Chemical, manager.session))
admin.add_view(ModelView(Species, manager.session))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
