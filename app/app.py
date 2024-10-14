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
def dayview():
    # TODO: Query what day number and day of the week we chose
    # TODO: Consider if using request.view_args is better (aka .../dayView/13) (now,  .../dayView?dayNum=13)
    #       Or maybe storing it locally is better?
    # TODO: Query all tasks for this day from the database
    # request.view_args['dayNum']
    return render_template('dayview.html', day_number=int(request.args['dayNum']), day_name='Logsday', month_name='October',
                           tasks={7:'Task for 7am'})

# a web page for adding a task
@app.route('/addTask', methods=['POST','GET'])
def add_event():
    return render_template('add_task.html', day_number=int(request.args['dayNum']), day_name='Logsday', month_name='October')

@app.route('/addTask/newTask', methods=['POST','GET'])
def receive_task():
    # request.form["task_name"]/request.form["from_time"]/request.form["to_time"]
    # can be used to get the name/from_time/to_time of the new event
    # TODO: ADD A NEW TASK TO THE DATABASE
    return redirect(url_for('index'))

# @app.route('/delete/<taskId>')
# def deleteTask(taskId):
#     mongo.db.tasks.delete_one({'_id': ObjectId(taskId)})
#     return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)