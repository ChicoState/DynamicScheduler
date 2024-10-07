from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os

app = Flask(__name__)

MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client.mydatabase

# a web page for viewing a month
@app.route('/', methods=['POST','GET'])
def calendar():
    return render_template('calendar.html')

# a web page for viewing the tasks for the day
@app.route('/dayview', methods=['POST', 'GET'])
def dayview():
    day = request.form['day']
    events = collection.find_one({'day': day})
    return render_template('dayview.html', day=day, events=events)

# a web page for adding a task
@app.route('/add_event', methods=['POST', 'GET'])
def add_event():
    day = request.form['day']
    event = request.form['event']
    collection.update_one({'day': day}, {'$push': {'events': event}}, upsert=True)
    return redirect(url_for('calendar'))

#@app.route('/addTask/newTask', methods=['POST','GET'])
#def receive_task():
    # request.form["task_name"]/request.form["from_time"]/request.form["to_time"]
    # can be used to get the name/from_time/to_time of the new event
    # TODO: ADD A NEW TASK TO THE DATABASE
    #return redirect(url_for('index'))

# @app.route('/delete/<taskId>')
# def deleteTask(taskId):
#     mongo.db.tasks.delete_one({'_id': ObjectId(taskId)})
#     return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)
