from app import db
from sqlalchemy.sql import func


class Roster(db.Model):
    __table_args__ = {'extend_existing': True}
    # See http://flask-sqlalchemy.pocoo.org/2.0/models/#simple-example
    # for details on the column types.

    # We always need an id
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    name = db.Column(db.String(100))
    real_name = db.Column(db.String(100))
    role = db.Column(db.String(100))    
    association = db.Column(db.String(100))
    accolade = db.Column(db.String(100))
    active = db.Column(db.String(100))
    finisher = db.Column(db.String(100))
    attack = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    health = db.Column(db.Integer)
    level = db.Column(db.Integer)
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    img = db.Column(db.String(1000))    

    def __repr__(self):
        return f'<Roster {self.name}>'

class Titles(db.Model):
    __table_args__ = {'extend_existing': True}
    # See http://flask-sqlalchemy.pocoo.org/2.0/models/#simple-example
    # for details on the column types.

    # We always need an id
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    name = db.Column(db.String(100))
    type = db.Column(db.String(100))
    association = db.Column(db.String(100))
    img = db.Column(db.String(1000))    

    def __repr__(self):
        return f'<Title {self.name}>'
    # def __init__(self, name, price, calories):
    #     se
    #     self.name = name
    #     self.real_name = real_name
    #     self.role = role
    #     self.association = association
    #     self.accolade = accolade
    #     self.active = active
    #     self.finisher = finisher
    #     self.attack = attack
    #     self.defense = defense
    #     self.health = health
    #     self.level = level
    #     self.wins = wins
    #     self.losses = losses
    #     self.img = img

    # def calories_per_dollar(self):
    #     if self.calories:
    #         return self.calories / self.price


# class Dessert(db.Model):
#     # See http://flask-sqlalchemy.pocoo.org/2.0/models/#simple-example
#     # for details on the column types.

#     # We always need an id
#     id = db.Column(db.Integer, primary_key=True)

#     # A dessert has a name, a price and some calories:
#     name = db.Column(db.String(100))
#     price = db.Column(db.Float)
#     calories = db.Column(db.Integer)

#     def __init__(self, name, price, calories):
#         self.name = name
#         self.price = price
#         self.calories = calories

#     def calories_per_dollar(self):
#         if self.calories:
#             return self.calories / self.price


# class Menu(db.Model):

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))

#     def __init__(self, name):
#         self.name = name


# def create_dessert(new_name, new_price, new_calories):
#     # Create a dessert with the provided input.
#     # At first, we will trust the user.

#     # This line maps to line 16 above (the Dessert.__init__ method)
#     dessert = Dessert(new_name, new_price, new_calories)

#     # Actually add this dessert to the database
#     db.session.add(dessert)

#     # Save all pending changes to the database
#     db.session.commit()

#     return dessert


if __name__ == "__main__":

    # Run this file directly to create the database tables.
    print("Creating database tables...")
    db.create_all()
    print("Done!")
