from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False, default=True)
    favorites = db.relationship('Favorites', backref='user')

    def __repr__(self):
        return '<Users %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username
            # do not serialize the password, it's a security breach
        }
    
class Peoples(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    birthday = db.Column(db.String(120), nullable=False)
    altura = db.Column(db.String(120), nullable=False)
    favorites = db.relationship('Favorites', backref='people')

    def __repr__(self):
        return '<Peoples %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birthday": self.birthday,
            "altura": self.altura
            # do not serialize the password, it's a security breach
        }
    
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    size = db.Column(db.String(120), nullable=False)
    population = db.Column(db.String(120), nullable=False)
    clima = db.Column(db.String(120), nullable=False)
    favorites = db.relationship('Favorites', backref='planet')

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "size": self.size,
            "population": self.population,
            "clima": self.clima
            # do not serialize the password, it's a security breach
        }
    
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=True)
    people_id = db.Column(db.Integer, db.ForeignKey('peoples.id'), nullable=True)

    def __repr__(self):
        return '<Favorites %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "people_id": self.people_id,
            # do not serialize the password, it's a security breach
        }
