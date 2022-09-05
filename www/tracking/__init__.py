#  Copyright (c) 2022. Wahinipa LLC
"""Initialize Flask app."""
import logging
import os
from os import environ

from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from tracking.commons.blueprint_registration import blueprint_registration

database = SQLAlchemy()
migrate = Migrate()

if os.getenv('DEBUG') != 'True':
    logging.basicConfig(filename='/home/willy/www/cupboard.log', level=logging.INFO)


def create_app():
    """Create Flask application."""
    application = Flask(__name__)
    configure_application(application)
    database.init_app(application)
    Bootstrap5(application)
    initialize_login_manager(application)
    from tracking.admin.administration import add_flask_admin
    add_flask_admin(application, database)
    with application.app_context():
        blueprint_registration(application)
        if not environ.get('SKIP_MODEL_LOAD') == 'True':
            import_models_and_initialize_database(database)
        if database.engine.url.drivername == 'sqlite':
            migrate.init_app(application, database, render_as_batch=True)
        else:
            migrate.init_app(application, database)
        return application


def configure_application(application):
    application.config.from_object('config.Config')
    application.config['BOOTSTRAP_SERVE_LOCAL'] = True  # This turns file serving static
    application.logger.setLevel(environ.get('LOGLEVEL', 'INFO').upper())
    db_echo = environ.get('DB_ECHO') == 'True'
    application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    application.config["SQLALCHEMY_ECHO"] = db_echo
    if db_echo:
        application.logger.info(f"Data is at {application.config['SQLALCHEMY_DATABASE_URI']}")


def initialize_login_manager(application):
    login_manager = LoginManager()
    login_manager.login_view = "people_bp.login"
    login_manager.init_app(application)
    from tracking.people.people_models import load_user
    login_manager.user_loader(load_user)


def import_models_and_initialize_database(database):
    # Using local imports helps break circularity of dependencies
    from tracking.admin.administration import initialize_database
    if environ.get('DB_INIT') or environ.get('TESTING'):
        print('initializing data base')
        initialize_database(database)


