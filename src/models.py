from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)    
    password = db.Column(db.String(80), unique=True, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favourite_characters = db.relationship('FavouriteCharacters', backref='user', lazy=True)
    favourite_planets = db.relationship('FavouritePlanets', backref='user', lazy=True)

    def __repr__(self):
        return self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email           
        }
    
class Characters(db.Model):
    __tablename__='characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)    
    gender = db.Column(db.String(250), nullable=False)
    favourite_character = db.relationship('FavouriteCharacters', backref='characters', lazy=True)    

    def __repr__(self):
        return '<Characters %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name            
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    __tablename__='planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    terrain = db.Column(db.String(80), unique=False, nullable=False)
    favourite_planets= db.relationship('FavouritePlantes', backref='planets', lazy=True)    

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.user_id            
        }

class FavouriteCharacters(db.Model):
    __tablename__='favouritecharacters'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    character_id= db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)    

    def __repr__(self):
        return str(self.id)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.user_id            
        }
    
class FavouritePlanets(db.Model):
    __tablename__='favouriteplanets'
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Interger, db.ForeignKey('planets.id'))
    user_id = db.Column(db.Interger, db.ForeignKey('user.id'), nullable=False)    

    def __repr__(self):
        return str(self.id)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.user_id            
        }