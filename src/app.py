import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Users, Planets, Peoples, Favorites

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_users():
    users = Users.query.all()
    all_users = [user.serialize() for user in users]
    return jsonify(all_users), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = Users.query.get(user_id)
    if user is None:
        raise APIException('User not found', status_code=404)
    return jsonify(user.serialize()), 200

@app.route('/users', methods=['POST'])
def add_user():
    request_data = request.get_json()
    if not request_data or 'email' not in request_data or 'username' not in request_data or 'password' not in request_data:
        raise APIException('Invalid request body', status_code=400)

    new_user = Users(email=request_data["email"], username=request_data["username"], password=request_data["password"])
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.serialize()), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    request_data = request.get_json()
    if not request_data:
        raise APIException('Invalid request body', status_code=400)

    user = Users.query.get(user_id)
    if user is None:
        raise APIException('User not found', status_code=404)

    if "username" in request_data:
        user.username = request_data["username"]

    if "email" in request_data:
        user.email = request_data["email"]

    if "password" in request_data:
        user.password = request_data["password"]

    db.session.commit()
    
    return jsonify(user.serialize()), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = Users.query.get(user_id)
    if user is None:
        raise APIException('User not found', status_code=404)

    db.session.delete(user)
    db.session.commit()
    
    return jsonify("User deleted successfully"), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    all_planets = [planet.serialize() for planet in planets]
    return jsonify(all_planets), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if planet is None:
        raise APIException('Planet not found', status_code=404)
    return jsonify(planet.serialize()), 200

@app.route('/people', methods=['GET'])
def get_people():
    people = Peoples.query.all()
    all_people = [person.serialize() for person in people]
    return jsonify(all_people), 200

@app.route('/people/<int:person_id>', methods=['GET'])
def get_person(person_id):
    person = Peoples.query.get(person_id)
    if person is None:
        raise APIException('Person not found', status_code=404)
    return jsonify(person.serialize()), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
