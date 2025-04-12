from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    # add relationship

    restaurant_pizzas = db.relationship ('restaurant_pizzas' , backref = 'restaurants')


    # add serialization rules

    def to_dict(self):
        return{
            'id': self.id,
            'name': self.name,
            'address': self.address
        }

    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # add relationship

    restaurant_pizzas = db.relationship ("restaurant_pizzas" , backref = 'pizza')

    # add serialization rules

    def to_dict(self):
        return{
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients
        }

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    # add relationships

    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable= False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'), nullable= False)

    # add serialization rules

    def to_dict(self):
        return{
            'id': self.id,
            'price': self.price,
            'restaurant_id': self.restaurant_id,
            'pizza_id': self.pizza_id,
        }

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
