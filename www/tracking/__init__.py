# Copyright 2022 Wahinipa LLC
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()
migrate = Migrate()
