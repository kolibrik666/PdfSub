from flask import Flask, json, jsonify, request
from pymongo import MongoClient
from flask_pymongo import pymongo
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import jwt
from bson import ObjectId
from functools import wraps
from datetime import datetime, timedelta, timezone
from gridfs import GridFS
from werkzeug.utils import secure_filename


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
fs = GridFS(db)
users_collection = pymongo.collection.Collection(db, "users")
papers_collection = pymongo.collection.Collection(db, "papers")

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
    hashed_password = bcrypt.generate_password_hash(password)

    user = {
        'email': email,
        'password': hashed_password.decode('utf-8'),
        'name': name,
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
        '_id': 1,
        'name': 1,
        'email': 1,
        'password': 1,
        'roles.isAdmin': 1,
        'roles.isParticipant': 1,
        'roles.isReviewer': 1
    }))
    users = [convert_to_json_compatible(user) for user in users]
    return jsonify(users)

@app.route('/api/users/<string:id>', methods=['GET'])
def get_user_by_id(id):
    try:
        # Validate and convert to ObjectId
        user = users_collection.find_one({'_id': ObjectId(id)})
        if user:
            return jsonify(convert_to_json_compatible(user)), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': 'Invalid User ID format or user not found'}), 400

def convert_to_json_compatible(doc):
    """Convert MongoDB document to a JSON-compatible format."""
    if isinstance(doc, list):
        # Recursively handle each element in the list
        return [convert_to_json_compatible(item) for item in doc]
    elif isinstance(doc, dict):
        # Process each key-value pair
        return {key: convert_to_json_compatible(value) for key, value in doc.items()}
    elif isinstance(doc, ObjectId):
        # Convert ObjectId to string
        return str(doc)
    elif isinstance(doc, datetime):
        # Convert datetime to ISO8601 string
        return doc.isoformat()
    else:
        # Return the value as is for other types
        return doc



@app.route('/api/publications', methods=['GET'])
def get_publications():
    publications = list(papers_collection.find({}, {
        '_id': 1,
        'title': 1,
        'authorId': 1,
        'co_authors': 1,
        'review_status': 1,
        'reviewerId': 1,
        'submit_status': 1,
        'submissionDate': 1,
        'rating': 1,
        'fileId': 1,
    }))
    publications = [convert_to_json_compatible(pub) for pub in publications]
    return jsonify(publications)

@app.route('/api/publications/<string:id>', methods=['GET'])
def get_publication(id):
    try:
        publication = papers_collection.find_one({'_id': ObjectId(id)})
        if publication:
            return jsonify(convert_to_json_compatible(publication)), 200
        else:
            return jsonify({'message': 'Publication not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/publications/<string:id>', methods=['PUT'])
def update_publication(id):
    data = request.get_json()
    update_fields = {}

    if 'reviewerId' in data:
        print("Sme na Reviewer ID:", data['reviewerId'])
        update_fields['reviewerId'] = data['reviewerId']

    papers_collection.update_one({'_id': ObjectId(id)}, {'$set': update_fields})
    return jsonify({'message': 'Publication updated successfully'}), 200

@app.route('/api/publications/file/<string:file_id>', methods=['GET'])
def get_publication_file(file_id):
    try:
        # Retrieve the file from GridFS
        file = fs.get(ObjectId(file_id))
        return app.response_class(
            file.read(),
            mimetype=file.content_type,
            headers={"Content-Disposition": f"attachment;filename={file.filename}"}
        )
    except Exception as e:
        return jsonify({'error': 'File not found or invalid ID'}), 404

@app.route('/api/publications/<string:id>/comments', methods=['POST'])
def add_comment(id):
    try:
        data = request.json
        print("Received data:", data)
        reviewer_id = data.get('reviewerId')
        comments = data.get('comments')

        if not reviewer_id or not comments:
            return jsonify({"error": "ReviewerId and comments are required"}), 400

        try:
            reviewer_id = reviewer_id
        except Exception as e:
            return jsonify({"error": "Invalid reviewerId format"}), 400

        new_comment = {
            "reviewerId": reviewer_id,
            "comments": comments,
            "submittedAt": datetime.utcnow().isoformat()
        }

        papers_collection.update_one(
            {"_id": ObjectId(id)},
            {"$push": {"feedback": new_comment}}
        )

        return jsonify({"message": "Feedback added successfully", "feedback": new_comment}), 201
    except Exception as e:
        print("Error:", str(e))  # Log any exceptions
        return jsonify({"error": str(e)}), 400

@app.route('/reviews', methods=['POST'])
def submit_review():
    data = request.json  # Get the data from the client
    publication_id = data.get('publicationId')
    review = data.get('review')

    if not publication_id or not review:
        return jsonify({"error": "Publication ID and review are required"}), 400

    # Example: Update the review status and details for the publication in MongoDB
    
    result = papers_collection.update_one(
        {"_id": ObjectId(publication_id)},  # Convert the string to ObjectId
        {
            "$set": {
                "review_status": "done",
               # "review_details": review,  # Store the review details
            }
        }
    )

    if result.matched_count == 1:  # Check if a document was updated
        return jsonify({"message": "Review submitted successfully."}), 200
    else:
        return jsonify({"error": "Publication not found"}), 404
    

@app.route('/api/publications/upload', methods=['POST'])
def upload_publication():
    try:
        title = request.form.get('title')
        author_id = request.form.get('authorId')
        file = request.files.get('file')
        co_authors = request.form.get('co_authors')

        if not (title and author_id and file):
            return jsonify({'error': 'Missing title, authorId, or file'}), 400

        file_id = fs.put(file, filename=file.filename, content_type=file.content_type)

        publication = {
            'title': title,
            'authorId': ObjectId(author_id),
            'fileId': str(file_id),  # Save file ID as a string
            'co_authors': co_authors,
            'submissionDate': datetime.utcnow().strftime('%B %d, %Y'),
            'review_status': 'pending',
        }
        papers_collection.insert_one(publication)

        # Convert ObjectId fields to strings for JSON serialization
        publication['_id'] = str(publication.get('_id', ''))
        publication['authorId'] = str(publication['authorId'])

        return jsonify({'message': 'Upload successful', 'publication': publication}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/publications/<string:id>', methods=['DELETE'])
def delete_publication(id):
    try:
        # Find the publication
        publication = papers_collection.find_one({'_id': ObjectId(id)})
        if not publication:
            return jsonify({'error': 'Publication not found'}), 404

        # Delete the file from GridFS
        fs.delete(ObjectId(publication['fileId']))

        # Delete the publication from the database
        papers_collection.delete_one({'_id': ObjectId(id)})

        return jsonify({'message': 'Publication deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/conferences', methods=['GET'])
def get_conferences():
    try:
        conferences = list(db['conferences'].find({}))
        for conf in conferences:
            conf['_id'] = str(conf['_id'])  # Convert ObjectId to string
            conf['start_date'] = conf['start_date'].strftime("%Y-%m-%d")  # Format to YYYY-MM-DD
            conf['end_date'] = conf['end_date'].strftime("%Y-%m-%d")  # Format to YYYY-MM-DD

        return jsonify(conferences), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/conferences/<string:id>', methods=['GET'])
def get_conference_details(id):
    try:
        conference = db['conferences'].find_one({'_id': ObjectId(id)})
        if conference:
            return jsonify(convert_to_json_compatible(conference)), 200
        else:
            return jsonify({'message': 'Conference not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/conferences', methods=['POST'])
def create_conference():
    try:
        data = request.get_json()
        name = data.get('name')
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        # Validate required fields
        if not name or not start_date or not end_date:
            return jsonify({"error": "Name, start_date, and end_date are required"}), 400

        # Convert date strings to datetime objects
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")

        new_conference = {
            'name': name,
            'start_date': start_date_obj,
            'end_date': end_date_obj,
        }

        db['conferences'].insert_one(new_conference)
        return jsonify({"message": "Conference created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)