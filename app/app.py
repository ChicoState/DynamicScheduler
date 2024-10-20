from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os

app = Flask(__name__)
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client.mydatabase

# Initialize collections
tasks_collection = db.tasks

# Ensure indexes for better performance
tasks_collection.create_index("day_number")

# a web page for viewing a month
@app.route('/', methods=['POST', 'GET'])
def index():
    # TODO: put in the correct month and day offset/num/last month, etc
    return render_template('calendar.html',
                           action_name='dayView', first_day_offset=2, num_days=31,
                           month_name='October', last_month_days=30)

# a web page for viewing the tasks for the day
@app.route('/dayView', methods=['POST', 'GET'])
def day_view():
    day_number = int(request.args.get('dayNum', 1))
    # Query all tasks for this day from the database
    tasks = list(tasks_collection.find({"day_number": day_number}))
    return render_template('dayView.html', day_number=day_number, day_name='Logsday', month_name='October', military_time=False, tasks=tasks)

# a web page for adding a task
@app.route('/addTask', methods=['POST', 'GET'])
def add_event():
    return render_template('addTask.html', day_number=int(request.args['dayNum']), day_name='Logsday', month_name='October')

@app.route('/addTask/newTask', methods=['POST', 'GET'])
def receive_task():
    # request.form["task_name"]/request.form["from_time"]/request.form["to_time"]
    # can be used to get the name/from_time/to_time of the new event
    task_name = request.form["task_name"]
    from_time = int(request.form["from_time"])
    to_time = int(request.form["to_time"])
    day_number = int(request.args['dayNum'])
    
    # ADD A NEW TASK TO THE DATABASE
    task = {
        "title": task_name,
        "start_time": from_time,
        "duration": to_time - from_time,
        "day_number": day_number,
        "is_task": True
    }
    tasks_collection.insert_one(task)
    
    return redirect(url_for('index'))

# a web page for viewing a task
@app.route('/viewTask', methods=['POST', 'GET'])
def view_task():
    # request.args['taskId'] to get the id of the task being displayed
    task_id = request.args['taskId']
    task = tasks_collection.find_one({"_id": task_id})
    # ARGS TO RENDER_TEMPLATE ARE NOT FINAL
    return render_template('viewTask.html', task=task)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
