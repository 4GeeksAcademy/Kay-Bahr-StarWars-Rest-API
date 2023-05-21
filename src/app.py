"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
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

    return jsonify(person), 200

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
        raise APIException("User not found", status_code=404)

    return jsonify(planet), 200

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
def handle_favorites():

    favorites = Favorites.query.all()
    all_favorites = list(map(lambda x: x.serialize(), favorites))

    return jsonify(all_favorites), 200

# # [POST] /favorite/starship/<int:starship_id> Add a new favorite starship to the current user with the starship id = starship_id.

@app.route('/favorite/starship/<int:starship_id>', methods=['POST'])
def create_favorite_starship(starship_name):

    request_body_fav_star = request.get_json()
    starship_name = request_body_fav_star["starship_name"]
    favorite_id = request_body_fav_star["favorite_id"]

    fav_star = Favorites.query.filter_by(starship_name= starship_name, favorite_id= favorite_id)
    if fav_star is None:
        fav_star = Favorites(starship_name= starship_name, favorite_id= favorite_id)
        db.session.add()
    else:
        fav_star = request_body_fav_star[starship_name]
    db.session.commit()

    return jsonify(fav_star), 200

# # [POST] /favorite/planet/<int:planet_id> Add a new favorite planet to the current user with the planet id = planet_id.

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def create_favorite_planet(planet_name):

    request_body_fav_planet = request.get_json()
    planet_name = request_body_fav_planet["planet_name"]
    favorite_id = request_body_fav_planet["favorite_id"]

    fav_planet = Favorites.query.filter_by(planet_name= planet_name, favorite_id= favorite_id)
    if fav_planet is None:
        fav_planet = Favorites(planet_name= planet_name, favorite_id= favorite_id)
        db.session.add()
    else:
        fav_planet = request_body_fav_planet[planet_name]
    db.session.commit()

    return jsonify(fav_planet), 200

# # [POST] /favorite/people/<int:people_id> Add new favorite people to the current user with the people id = people_id.

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def create_favorite_people(people_name):

    request_body_fav_person = request.get_json()
    people_name = request_body_fav_person["people_name"]
    favorite_id = request_body_fav_person["favorite_id"]

    fav_person = Favorites.query.filter_by(people_name= people_name, favorite_id= favorite_id)
    if fav_person is None:
        fav_person = Favorites(people_name= people_name, favorite_id= favorite_id)
        db.session.add()
    else:
        fav_person = request_body_fav_person[people_name]
    db.session.commit()

    return jsonify(fav_person), 200

# # [DELETE] /favorite/planet/<int:planet_id> Delete favorite planet with the id = planet_id.

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_name):

    fav_planet = Favorites.query.get(planet_name)
    if fav_planet is None:
        raise APIException("Favorite planet not found", status_code=404)
    db.session.delete(fav_planet)
    db.session.commit()

    return jsonify("Favorite planet deletion successful"), 200

# # [DELETE] /favorite/people/<int:people_id> Delete favorite people with the id = people_id.

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_name):

    fav_person = Favorites.query.get(people_name)
    if fav_person is None:
        raise APIException("Favorite person not found", status_code=404)
    db.session.delete(fav_person)
    db.session.commit()

    return jsonify("Favorite person deletion successful"), 200

@app.route('/favorite/starship/<int:starship_id>', methods=['DELETE'])
def delete_favorite_starship(starship_name):

    fav_starship = Favorites.query.get(starship_name)
    if fav_starship is None:
        raise APIException("Favorite starship not found", status_code=404)
    db.session.delete(fav_starship)
    db.session.commit()

    return jsonify("Favorite starship deletion successful"), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)