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
from models import db, Users, Characters, Planets
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

@app.route('/users', methods=['GET'])
def get_all_users():

    all_users = Users.query.all()
    all_users = list(map(lambda x: x.serialize(), all_users))

    print('GET Rerquest: All the USERS ====>', all_users)

    return jsonify(all_users), 200

@app.route('/users/favourites', methods=['GET'])
def get_favourites():

    response_body = {
        "msg": "Hello, this is your GET /users/favourites response "
    }

    return jsonify(response_body), 200

@app.route('/characters', methods=['GET'])
def get_all_characters():

    all_characters = Characters.query.all()
    all_characters = list(map(lambda x: x.serialize(), all_characters))

    print('GET Request: All the PEOPLE ====>', all_characters)

    return jsonify(all_characters), 200

@app.route('/characters/<init:id', methods=['GET'])
def get_single_character(id):

    character = Characters.query.get(id)
    print (character.serialize())

    print('GET Request: Getting an idividual character', character)

    return jsonify(character.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_all_planets():

    all_planets = Planets.query.all()
    all_planets = list(map(lambda x: x.serialize(), all_planets))

    print('GET Request: All the PLANETS ====>', all_planets)

    return jsonify(all_planets), 200

@app.route('/planets/<init:id', methods=['GET'])
def get_single_planet(id):

    planet = Planets.query.get(id)
    print(planet.serialize())

    print('GET Request: Getting an idividual planet', planet)

    return (jsonify.serialize()), 200   

    
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
