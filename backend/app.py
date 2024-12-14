from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_pymongo import pymongo
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import jwt

from bson import ObjectId
from functools import wraps
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})
bcrypt = Bcrypt(app)
secret = "***************"

@app.route('/')
def hello():
    return 'Hello from Flask!'

CONNECTION_STRING ="mongodb+srv://nbusr:nbusr123@cluster0.n5md3.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(CONNECTION_STRING, ssl=True)

# article_collection = pymongo.collection.Collection(db, "articles")

db = client.get_database("pdf")
users_collection = pymongo.collection.Collection(db, "users")

@app.route('/api/decode-token', methods=['POST'])
def decode_token():
    try:
        data = request.get_json()
        token = data.get('token')
        if not token:
            return jsonify({"error": "Token is missing"}), 400

        decoded_data = jwt.decode(token, secret, algorithms=["HS256"])
        return jsonify(decoded_data), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    res_data = {}

    user = users_collection.find_one({'email': email})
    if user and bcrypt.check_password_hash(user['password'], password):
        time = datetime.utcnow() + timedelta(hours=24)
        token = jwt.encode({
            "user": {
                "email": f"{user['email']}",
                "id": f"{user['_id']}",
                "isAdmin": user['roles'].get('isAdmin', False),
                "isParticipant": user['roles'].get('isParticipant', False),
                "isReviewer": user['roles'].get('isReviewer', False)
            },
            "exp": time
        }, secret)
        return jsonify({
            'message': 'Login successful',
            'isAdmin': user['roles'].get('isAdmin', False),
            'isParticipant': user['roles'].get('isParticipant', False),
            'isReviewer': user['roles'].get('isReviewer', False),
            'token': token
        }), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    surname = data.get('surname')
    hashed_password = bcrypt.generate_password_hash(password)

    user = {
        'email': email,
        'password': hashed_password.decode('utf-8'),
        'name': name,
        'surname': surname,
        'roles': {'isAdmin': False, 'isParticipant': False, 'isReviewer': False},
        'conferences': [],
        'papers': []
    }

    users_collection.insert_one(user)
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/users/<string:email>', methods=['PUT'])
def update_user(email):
    data = request.get_json()
    update_fields = {}

    if 'name' in data:
        update_fields['name'] = data['name']
    if 'surname' in data:
        update_fields['surname'] = data['surname']
    if 'roles' in data:
        if 'isAdmin' in data['roles']:
            update_fields['roles.isAdmin'] = data['roles']['isAdmin']
        if 'isParticipant' in data['roles']:
            update_fields['roles.isParticipant'] = data['roles']['isParticipant']
        if 'isReviewer' in data['roles']:
            update_fields['roles.isReviewer'] = data['roles']['isReviewer']

    users_collection.update_one({'email': email}, {'$set': update_fields})
    return jsonify({'message': 'User updated successfully'}), 200

@app.route('/api/users/<string:email>', methods=['DELETE'])
def delete_user(email):
    result = users_collection.delete_one({'email': email})
    if result.deleted_count == 1:
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/api/users', methods=['GET'])
def get_users():
    users = list(users_collection.find({}, {
        '_id': 0,
        'surname': 1,
        'name': 1,
        'email': 1,
        'password': 1,
        'roles.isAdmin': 1,
        'roles.isParticipant': 1,
        'roles.isReviewer': 1
    }))
    return jsonify(users)

@app.route('/api/publications', methods=['GET'])
def get_publications():
    publications = [
        {'id': 1, 'title': 'Publication 1', 'authors': ['Author 1', 'Author 2'], 'reviewer': 'Reviewer 1', 'abstract': 'Abstract 1', 'status': 'drafted'},
        {'id': 2, 'title': 'Publication 2', 'authors': ['Author 3'], 'reviewer': 'Reviewer 2', 'abstract': 'Abstract 2', 'status': 'submitted'},
    ]
    return jsonify(publications)

@app.route('/api/publications/<int:id>', methods=['GET'])
def get_publication(id):
    publications = [
        {'id': 1, 'title': 'Publication 1', 'authors': ['Author 1', 'Author 2'], 'reviewer': 'Reviewer 1', 'abstract': 'Abstract 1', 'status': 'drafted'},
        {'id': 2, 'title': 'Publication 2', 'authors': ['Author 3'], 'reviewer': 'Reviewer 2', 'abstract': 'Abstract 2', 'status': 'submitted'},
    ]
    publication = next((pub for pub in publications if pub['id'] == id), None)
    return jsonify(publication)

if __name__ == '__main__':
    app.run(debug=True)