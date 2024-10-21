from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os

app = Flask(__name__)

MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client.mydatabase

# a web page for viewing a month
@app.route('/', methods=['POST','GET'])
def index():
    # TODO: put in the correct month and day offset/num/last month, etc
    return render_template('calendar.html', 
                           action_name='dayView', first_day_offset=2, num_days=31, 
                           month_name='October', last_month_days=30)

# a web page for viewing the tasks for the day
@app.route('/dayView', methods=['POST','GET'])
def day_view():
    # TODO: Query what day number and day of the week we chose
    # TODO: Consider if using request.view_args is better (aka .../dayView/13) (now,  .../dayView?dayNum=13)
    #       Or maybe storing it locally is better?
    # TODO: Query all tasks for this day from the database
    # request.view_args['dayNum']
    return render_template('dayView.html', day_number=int(request.args['dayNum']), day_name='Logsday', month_name='October',
                           military_time=False,
                           tasks=[
                               {"start_time": 120, "duration": 60, "title": "from 2 to 3", "id": "event1", "is_task": False},
                               {"start_time": 180, "duration": 30, "title": "from 3 to 3:30", "id": "task1", "is_task": True},
                               {"start_time": 1200, "duration": 240, "title": "from 20 to 24", "id": "event2", "is_task": False}
                            ])

# a web page for adding a task
@app.route('/addTask', methods=['POST','GET'])
def add_event():
    return render_template('addTask.html', day_number=int(request.args['dayNum']), day_name='Logsday', month_name='October')

@app.route('/addTask/newTask', methods=['POST','GET'])
def receive_task():
    # request.form["task_name"]/request.form["from_time"]/request.form["to_time"]
    # can be used to get the name/from_time/to_time of the new event
    # TODO: ADD A NEW TASK TO THE DATABASE
    return redirect(url_for('index'))

@app.route('/viewTask', methods=['POST','GET'])
def view_task():

    task_id = request.args.get('taskId')  # Retrieved from query string (GET part)
    day_name = request.form.get('day_name')  # Retrieved from form (POST part)
    month_name = request.form.get('month_name')
    day_number = request.form.get('day_number')
    # Render the template with these values
    return render_template('viewTask.html', 
                           action_name='dayView',
                           task_id=task_id, 
                           day_number=day_number, 
                           day_name=day_name , 
                           month_name=month_name,
                           military_time=False)
    # request.args['taskId'] to get the id of the task being displayed
    # TODO: Make this page: it's empty rn
    # ARGS TO RENDER_TEMPLATE ARE NOT FINAL"
    # return render_template('viewTask.html', task_id=request.args['taskId'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)