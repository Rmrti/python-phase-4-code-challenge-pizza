#!/usr/bin/env python3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_migrate import Migrate
from flask import Flask, jsonify, request, make_response
from flask_restful import Api, Resource

import os
metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)
migrate = Migrate()

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")




def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.json.compact = False

    db.init_app(app)
    migrate.init_app(app, db)

    from server.models import Restaurant, Pizza, RestaurantPizza

    #Route for homepage
    @app.route("/")
    def index():
        return "<h1>Code challenge</h1>"
    
    # GET /restaurant
    @app.route('/restaurant', methods = ['GET'])
    def get_restaurants():
        restaurants = Restaurant.query.all()
        return jsonify([restaurant.to_dict(only=("id", "name", "address")) for restaurant in restaurants]), 200

    
    
    return app










