from app import db
from sqlalchemy.sql import func
from flask_login import UserMixin

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

class Fueds(db.Model):
    __table_args__ = {'extend_existing': True}
    # See http://flask-sqlalchemy.pocoo.org/2.0/models/#simple-example
    # for details on the column types.

    # We always need an id
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    participant_1 = db.Column(db.String(100))
    participant_2 = db.Column(db.String(100))
    popularity = db.Column(db.String(100))
    status = db.Column(db.String(100))    
    company = db.Column(db.String(100))    

    def __repr__(self):
        return f'<Fueds {self.id}>'

class Companies(db.Model):
    __table_args__ = {'extend_existing': True}
    # See http://flask-sqlalchemy.pocoo.org/2.0/models/#simple-example
    # for details on the column types.

    # We always need an id
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    name = db.Column(db.String(100))
    img = db.Column(db.String(100))

    def __repr__(self):
        return f'<Companies {self.name}>'

class Result(db.Model):
    __table_args__ = {'extend_existing': True}
    # See http://flask-sqlalchemy.pocoo.org/2.0/models/#simple-example
    # for details on the column types.

    # We always need an id
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    result = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    rating = db.Column(db.Integer)

    def __repr__(self):
        return f'<Results {self.id}>'

class User(UserMixin,db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


if __name__ == "__main__":

    # Run this file directly to create the database tables.
    print("Creating database tables...")
    db.create_all()
    print("Done!")
