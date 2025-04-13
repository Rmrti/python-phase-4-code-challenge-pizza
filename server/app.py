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
    
    # GET /restaurants
    @app.route('/restaurants', methods = ['GET'])
    def get_restaurants():
        restaurants = Restaurant.query.all()
        return jsonify([restaurant.to_dict(only=("id", "name", "address")) for restaurant in restaurants]), 200
    
    #GET /restaurants/<int:id
    @app.route('/restaurants/<int:id>', methods = ['GET'])
    def get_restaurant(id):
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return  jsonify({'error': "Restaurant not found"}),404
        return jsonify(restaurant.to_dict()), 200
    
    #CREATE /restaurants
    @app.route('/restaurants', methods = ['POST'])
    def create_restaurant():
        data = request.get_json()

        try:
            restaurant = Restaurant(
                name=data['name'],
                address=data['address']

            )
            db.session.add(restaurant)
            db.session.commit()
            
            return jsonify(restaurant.to_dict()), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({"error" : str(e)}), 400
        except ValueError as e:
            db.session.rollback()
            return jsonify({"errors": ["validation errors"]}), 400
        
    #DELETE /restaurants/<int:id
    @app.route('/restaurants/<int:id>', methods = ['DELETE'])
    def delete_restaurant(id):
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return jsonify ({'error':'restaurant not found'}),404
        
        db.session.delete(restaurant)
        db.session.commit()
        return '',204
    
    #GET /pizzas
    @app.route('/pizzas', methods = ['GET'])
    def get_pizzas():
        pizzas = Pizza.query.all()
        return jsonify ([pizza.to_dict()for pizza in pizzas])
    
    #POST /pizzas
    @app.route('/pizzas', methods = ['POST'])
    def create_pizza():
        data = request.get_json()

        try:
            pizza = Pizza(
                name=data['name'],
                ingredients=data['ingredients']

            )
            db.session.add(pizza)
            db.session.commit()
            
            return jsonify(pizza.to_dict()), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({"error" : str(e)}), 400
        except ValueError as e:
            db.session.rollback()
            return jsonify({"errors": ["validation errors"]}), 400

    
     #POST /restaurant_pizzas
    @app.route('/restaurant_pizzas', methods = ['POST'])
    def create_restaurant_pizza():
        data = request.get_json()

        try:
            restaurant_pizza = RestaurantPizza(
                price=data['price'],
                pizza_id=data['pizza_id'],
                restaurant_id = data['restaurant_id']

            )
            db.session.add(restaurant_pizza)
            db.session.commit()
            
            return jsonify(restaurant_pizza.to_dict()), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({"error" : str(e)}), 400
        except ValueError as e:
            db.session.rollback()
            return jsonify({"errors": ["validation errors"]}), 400

    
    return app










