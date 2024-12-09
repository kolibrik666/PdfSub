from flask import Flask, jsonify
from pymongo import MongoClient
from flask_pymongo import pymongo
from flask_cors import CORS

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