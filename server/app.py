#!/usr/bin/env python3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os
metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.json.compact = False

    db.init_app(app)
    migrate.init_app(app, db)  # ← Add this line
    return app


# @app.route("/")
# def index():
#     return "<h1>Code challenge</h1>"


