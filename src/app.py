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
from models import db, Users, Planets, Peoples, Favorites
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
def get_users():

    users = Users.query.all()
    all_users = list(map(lambda item: item.serialize(), users))

    return jsonify(all_users), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_id(user_id):

    # user = Users.query.all()
    elegido = Users.query.filter_by(id=user_id).first()
    if elegido is None:
        raise APIException('Usuario no existe', status_code=404)
    
    return jsonify(elegido.serialize()), 200

@app.route('/user', methods=['POST'])
def add_user():
    request_body_user = request.get_json()
    new_user = Users(email=request_body_user["email"], username=request_body_user["username"],password=request_body_user["password"])
    db.session.add(new_user)
    db.session.commit()

    return jsonify(request_body_user), 200

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):

    request_body_user = request.get_json()

    elegido = Users.query.get(user_id)

    if elegido is None:
        raise APIException('Usuario no existe', status_code=404)
    
    if "username" in request_body_user:
        elegido.username = request_body_user["username"]

    if "email" in request_body_user:
        elegido.email = request_body_user["email"]

    if "password" in request_body_user:
        elegido.password = request_body_user["password"]
    
    return jsonify(elegido.serialize()), 200

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):

    elegido = Users.query.get(user_id)

    if elegido is None:
        raise APIException('Usuario no existe', status_code=404)
    
    db.session.delete(elegido)
    db.session.commit()
    
    return jsonify("OK"), 200

@app.route('/planets', methods=['GET'])
def get_planets():

    planets = Planets.query.all()
    all_planets = list(map(lambda item: item.serialize(), planets))

    return jsonify(all_planets), 200

@app.route('/user/<int:planet_id>', methods=['GET'])
def get_planet_id(planet_id):

    elegido = Planets.query.filter_by(id=planet_id).first()
    if elegido is None:
        raise APIException('Planeta no existe', status_code=404)
    
    return jsonify(elegido.serialize()), 200

@app.route('/people', methods=['GET'])
def get_people():

    people = Peoples.query.all()
    all_people = list(map(lambda item: item.serialize(), people))

    return jsonify(all_people), 200

@app.route('/user/<int:people_id>', methods=['GET'])
def get_people_id(people_id):

    elegido = Peoples.query.filter_by(id=people_id).first()
    if elegido is None:
        raise APIException('Planeta no existe', status_code=404)
    
    return jsonify(elegido.serialize()), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
