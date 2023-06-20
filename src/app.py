"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Starships, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# # Create an API that connects to a database and implements the following Endpoints (very similar to SWAPI.dev or SWAPI.tech):

# # [GET] /people Get a list of all the people in the database

@app.route('/people', methods=['GET'])
def handle_people():

    people = People.query.all()
    all_people = list(map(lambda x: x.serialize(), people))

    return jsonify(all_people), 200

# # [GET] /people/<int:people_id> Get a one single people information

@app.route('/people/<int:people_id>', methods=['GET'])
def handle_person(people_id):
    person = People.query.get(people_id)
    if person is None:
        raise APIException("User not found", status_code=404)
    return jsonify(person.serialize()), 200

# # [GET] /planets Get a list of all the planets in the database

@app.route('/planets', methods=['GET'])
def handle_planets():

    planets = Planets.query.all()
    all_planets = list(map(lambda x: x.serialize(), planets))

    return jsonify(all_planets), 200

# # [GET] /planets/<int:planet_id> Get one single planet information

@app.route('/planets/<int:planet_id>', methods=['GET'])
def handle_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if planet is None:
        raise APIException("Planet not found", status_code=404)
    return jsonify(planet.serialize()), 200

# # [GET] /starships Get a list of all the starships in the database

@app.route('/starships', methods=['GET'])
def handle_starships():

    starships = Starships.query.all()
    all_starships = list(map(lambda x: x.serialize(), starships))

    return jsonify(all_starships), 200

# # [GET] /starships/<int:starship_id> Get one single starship information

@app.route('/starships/<int:starship_id>', methods=['GET'])
def handle_starship(starship_id):

    starship = Starships.query.get(starship_id)
    if starship is None:
        raise APIException("User not found", status_code=404)

    return jsonify(starship), 200

# # Additionally create the following endpoints to allow your StartWars blog to have users and favorites:

# # [GET] /users Get a list of all the blog post users

@app.route('/users', methods=['GET'])
def handle_users():

    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))

    return jsonify(all_users), 200

@app.route('/users', methods=['POST'])
def create_users():

    request_body_users = request.get_json()

    user1 = User(first_name=request_body_users["first_name"], last_name=request_body_users["last_name"], email=request_body_users["email"], password=request_body_users["password"])
    db.session.add(user1)
    db.session.commit()

    return jsonify(request_body_users), 200

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_users(user_id):

    request_body_users = request.get_json()

    user1 = User.query.get(user_id)
    if user1 is None:
        raise APIException("User not found", status_code=404)
    if "username" in request_body_users:
        user1.username = request_body_users["username"]
    if "first_name" in request_body_users:
        user1.first_name = request_body_users["first_name"]
    if "last_name" in request_body_users:
        user1.first_name = request_body_users["last_name"]
    if "email" in request_body_users:
        user1.first_name = request_body_users["email"]
    
    db.session.commit()

    return jsonify(request_body_users), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):

    user1 = User.query.get(user_id)
    if user1 is None:
        raise APIException("User not found", status_code=404)
    db.session.delete(user1)
    db.session.commit()

    return jsonify("User deletion successful"), 200

# # [GET] /users/favorites Get all the favorites that belong to the current user.

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.args.get('user_id')
    favorites = Favorites.query.filter_by(user_id=user_id).all()
    serialized_favorites = [fav.serialize() for fav in favorites]
    return jsonify(serialized_favorites), 200


# # [POST] /favorite/starship/<int:starship_id> Add a new favorite starship to the current user with the starship id = starship_id.

@app.route('/favorite/starship/<int:starship_id>', methods=['POST'])
def add_favorite_starship(starship_id):
    user_id = get_current_user_id()
    starship = Starships.query.get(starship_id)
    
    if not starship:
        return jsonify({'message': 'Starship not found'}), 404
    
    favorite = Favorites(user_id=user_id, starship_id=starship_id)
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify({'message': 'Favorite starship added successfully'}), 201


# # [POST] /favorite/planet/<int:planet_id> Add a new favorite planet to the current user with the planet id = planet_id.

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = get_current_user_id()
    planet = Planets.query.get(planet_id)
    
    if not planet:
        return jsonify({'message': 'Planet not found'}), 404
    
    favorite = Favorites(user_id=user_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify({'message': 'Favorite planet added successfully'}), 201


# # [POST] /favorite/people/<int:people_id> Add new favorite people to the current user with the people id = people_id.

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user_id = get_current_user_id()
    people = People.query.get(people_id)
    
    if not people:
        return jsonify({'message': 'People not found'}), 404
    
    favorite = Favorites(user_id=user_id, people_id=people_id)
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify({'message': 'Favorite people added successfully'}), 201


# # [DELETE] /favorite/planet/<int:planet_id> Delete favorite planet with the id = planet_id.

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = get_current_user_id()
    favorite = Favorites.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    
    if not favorite:
        return jsonify({'message': 'Favorite planet not found'}), 404
    
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({'message': 'Favorite planet deleted successfully'}), 200

# # [DELETE] /favorite/people/<int:people_id> Delete favorite people with the id = people_id.

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    user_id = get_current_user_id()  # Implement this function to get the current user ID
    favorite = Favorites.query.filter_by(user_id=user_id, people_id=people_id).first()
    
    if not favorite:
        return jsonify({'message': 'Favorite people not found'}), 404
    
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({'message': 'Favorite people deleted successfully'}), 200

@app.route('/favorite/starship/<int:starship_id>', methods=['DELETE'])
def delete_favorite_starship(starship_id):
    user_id = get_current_user_id()
    favorite = Favorites.query.filter_by(user_id=user_id, starship_id=starship_id).first()
    
    if not favorite:
        return jsonify({'message': 'Favorite starship not found'}), 404
    
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({'message': 'Favorite starship deleted successfully'}), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_current_user_id():
    try:
        current_user_id = get_jwt_identity()
        return current_user_id
    except NoAuthorizationError:
        raise APIException("Authorization header is missing or invalid", status_code=401)

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)