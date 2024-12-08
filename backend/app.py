from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongo', 27017)  # Pripojenie na MongoDB (služba sa volá mongo)
db = client.test_database

@app.route('/')
def hello():
    return 'Hello from Flask!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
