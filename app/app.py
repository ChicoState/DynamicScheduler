from flask import Flask
from pymongo import MongoClient
import os

app = Flask(__name__)

MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client.mydatabase

#sample function
@app.route('/')
def index():
    return "Hello World!"

#calendar functions for dayview and calendar
@app.route('/')
def calendar():
    return render_template('calendar.html')

@app.route('/dayview', methods=['POST'])
def dayview():
    day = request.form['day']
    events = collection.find_one({'day': day})
    return render_template('dayview.html', day=day, events=events)

@app.route('/add_event', methods=['POST'])
def add_event():
    day = request.form['day']
    event = request.form['event']
    collection.update_one({'day': day}, {'$push': {'events': event}}, upsert=True)
    return redirect(url_for('calendar'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
