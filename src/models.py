from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class People():
    name = db.Column(db.String(120), unique=True, nullable=False)
    type = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "name": self.name,
            "type": self.type,
        }

class Planets():
    name = db.Column(db.String(120), unique=True, nullable=False)
    type = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "name": self.name,
            "type": self.type,
        }
    
class Starships():
    name = db.Column(db.String(120), unique=True, nullable=False)
    type = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Starships %r>' % self.name

    def serialize(self):
        return {
            "name": self.name,
            "type": self.type,
        }
    
class Favorites():
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User"))
    people_name = db.Column(db.String(80), db.ForeignKey("People"))
    planets_name = db.Column(db.String(80), db.ForeignKey("Planets"))
    starships_name = db.Column(db.String(80), db.ForeignKey("Starships"))

    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_name": self.people_name,
            "planets_name": self.planets_name,
            "starships_name": self.starships_name,
        }