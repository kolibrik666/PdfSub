from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_pymongo import pymongo
from flask_cors import CORS
import bcrypt

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return 'Hello from Flask!'

CONNECTION_STRING ="mongodb+srv://nbusr:nbusr123@cluster0.n5md3.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(CONNECTION_STRING, ssl=True)

# article_collection = pymongo.collection.Collection(db, "articles")

db = client.get_database("test")
users_collection = pymongo.collection.Collection(db, "users")

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = users_collection.find_one({'email': email})
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return jsonify({'message': 'Login successful', 'role': user['role']}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    surname = data.get('surname')
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    user = {
        'email': email,
        'password': hashed_password.decode('utf-8'),
        'name': name,
        'surname': surname,
        'role': 'student'  # default role
    }

    users_collection.insert_one(user)
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/users', methods=['GET'])
def get_users():
    users = list(users_collection.find({}, {'_id': 0, 'surname': 1, 'name': 1, 'email': 1, 'password': 1, 'role': 1}))
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