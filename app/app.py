from flask import Flask
from pymongo import MongoClient
import os

app = Flask(__name__)

MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client.mydatabase

@app.route('/')
def index():
    return "Hello World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)