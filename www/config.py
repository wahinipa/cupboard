#  Copyright (c) 2022, Wahinipa LLC
# """Flask configuration variables."""
from os import environ, path

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Set Flask configuration from .env file."""

    # General Config
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    # Database
    if environ.get('TESTING') == 'True':
        if environ.get('TEST_SQL_IN_MEMORY') == 'True':
            SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:" # 10x faster testing
        else:
            SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_TEST_URI")
    else:
        SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
