from flask import Flask, render_template, request
from pymongo import MongoClient
import os

app = Flask(__name__)

MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client.mydatabase

@app.route('/', methods=['POST','GET'])
def index():
    # return render_template('add_task.html')
    return render_template('calendar.html', 
                           action_name="dayView", first_day_offset=2, num_days=30, month_name="Logsday", last_month_days=31)

@app.route('/dayView', methods=['POST','GET'])
def dayview():
    return render_template('dayview.html')

@app.route('/addTask', methods=['POST','GET'])
def add_event():
    if request.method == 'POST':
        # request.form["ev_name"]/request.form["from_time"]/request.form["to_time"]
        # can be used to get the name/from_time/to_time of the new event
        return render_template('calendar.html', 
                                action_name="dayView", first_day_offset=2, num_days=30, month_name="Logsday", last_month_days=31)
    return render_template('add_task.html')

@app.route('/delete/<taskId>')
def deleteTask(taskId):
    mongo.db.tasks.delete_one({'_id': ObjectId(taskId)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# _______________________________________________________________________________

# from flask import Flask, render_template, request, redirect, url_for
# from flask_pymongo import PyMongo
# from datetime import datetime

# from pymongo import MongoClient
# import os

# app = Flask(__name__)
# # app.config['MONGO_URI'] = 'mongodb://localhost:27017/whatever'
# # mongo = PyMongo(app)
# MONGO_URI = os.getenv('MONGO_URI')
# client = MongoClient(MONGO_URI)
# db = client.mydatabase

# @app.route('/')
# def index():
#     return "Hello World! I have been changed!<button>lol</button>"
#     tasks = mongo.db.tasks.find().sort('dateTime', 1)
#     return render_template('calendar.html', tasks=tasks)

# @app.route('/add', methods=['POST'])
# def addTask():
#     title = request.form['title']
#     description = request.form['description']
#     dateTime = datetime.strptime(request.form['dateTime'], '%Y-%m-%d %H:%M:%S')
#     newTask = {'title': title, 'description': description, 'dateTime': dateTime}
#     mongo.db.tasks.insert_one(newTask)
#     return redirect(url_for('index'))

# @app.route('/delete/<taskId>')
# def deleteTask(taskId):
#     mongo.db.tasks.delete_one({'_id': ObjectId(taskId)})
#     return redirect(url_for('index'))

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
#     # app.run(debug=True)
