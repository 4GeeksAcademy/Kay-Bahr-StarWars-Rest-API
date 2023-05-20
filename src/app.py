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
from models import db, User
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

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)



# # # Create an API that connects to a database and implements the following Endpoints (very similar to SWAPI.dev or SWAPI.tech):

# # [GET] /people Get a list of all the people in the database

    # @app.route('/user', methods=['GET'])
    # def handle_user():

    #     response_body = {
    #         
    #     }

    #     return jsonify(response_body), 200


# # [GET] /people/<int:people_id> Get a one single people information

    # @app.route('/user', methods=['GET'])
    # def handle_people():

    #     response_body = {
    #         
    #     }

    #     return jsonify(response_body), 200


# # [GET] /planets Get a list of all the planets in the database

    # @app.route('/user', methods=['GET'])
    # def handle_planets():

    #     response_body = {
    #         
    #     }

    #     return jsonify(response_body), 200


# # [GET] /planets/<int:planet_id> Get one single planet information

    # @app.route('/user', methods=['GET'])
    # def handle_planet():

    #     response_body = {
    #         
    #     }

    #     return jsonify(response_body), 200


# # Additionally create the following endpoints to allow your StartWars blog to have users and favorites:

# # [GET] /users Get a list of all the blog post users

    # @app.route('/user', methods=['GET'])
    # def handle_users():

    #     response_body = {
    #         
    #     }

    #     return jsonify(response_body), 200


# # [GET] /users/favorites Get all the favorites that belong to the current user.

    # @app.route('/user', methods=['GET'])
    # def handle_favorites():

    #     response_body = {
    #         
    #     }

    #     return jsonify(response_body), 200


# # [POST] /favorite/planet/<int:planet_id> Add a new favorite planet to the current user with the planet id = planet_id.

    # @app.route('/user', methods=['POST'])
    # def create_favorite_planet():

    #     response_body = {
    #         
    #     }

    #     return jsonify(response_body), 200


# # [POST] /favorite/people/<int:people_id> Add new favorite people to the current user with the people id = people_id.

    # @app.route('/user', methods=['POST'])
    # def create_favorite_people():

    #     response_body = {
    #         
    #     }

    #     return jsonify(response_body), 200


# # [DELETE] /favorite/planet/<int:planet_id> Delete favorite planet with the id = planet_id.

    # @app.route('/user', methods=['DELETE'])
    # def delete_favorite_planet():

    #     response_body = {
    #         
    #     }

    #     return jsonify(response_body), 200


# # [DELETE] /favorite/people/<int:people_id> Delete favorite people with the id = people_id.

    # @app.route('/user', methods=['DELETE'])
    # def delete_favorite_people():

    #     response_body = {
    #         
    #     }

    #     return jsonify(response_body), 200


# # Your current API does not have an authentication system (yet), which is why the only way to create users is directly on the database using the flask admin.