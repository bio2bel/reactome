# -*- coding: utf-8 -*-

""" This module contains the flask-admin application to visualize the db"""

from .manager import Manager

if __name__ == '__main__':
    manager = Manager()
    app = manager.get_flask_admin_app()
    app.secret_key = 'a\x1c\xd4\x1b\xb1\x05\xac\xac\xee\xcb6\xd8\x9fl\x14%B\xd2W\x9fP\x06\xcb\xff'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True, host='0.0.0.0', port=5000)
