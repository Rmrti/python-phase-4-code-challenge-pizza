
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from .app import db


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    # add relationship

    restaurant_pizzas = db.relationship ('RestaurantPizza' , backref = 'restaurants', cascade = "all, delete")


    # add serialization rules

    pizzas = association_proxy('restaurant_pizzas', 'pizza')
    serialize_rules = ('-restaurant_pizzas.restaurant',)

    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # add relationship

    restaurant_pizzas = db.relationship ("RestaurantPizza" , backref = 'pizza')

    # add serialization rules

    restaurants = association_proxy('restaurant_pizzas', 'restaurant')
    serialize_rules = ('-restaurant_pizzas.pizza',)

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    # add relationships

    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable= False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable= False)

    # add serialization rules

    serialize_rules = ('-restaurant.restaurant_pizzas', '-pizza.restaurant_pizzas')


    # add validation

    def validate(self):
        if not self.restaurant_id:
            raise ValueError('Restaurant id is missing')
        if not self.pizza_id:
            raise ValueError('Pizza id is missing')
        if self.price < 1 or self.price > 30:
            raise ValueError("Price should be between 1 and 30")
        
    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"
