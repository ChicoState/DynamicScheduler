from flask import Flask, render_template, request, redirect, url_for
import os
from bson.objectid import ObjectId
import db

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('calendar.html',
                           action_name='dayView', first_day_offset=2, num_days=31,
                           month_name='October', last_month_days=30)

@app.route('/dayView', methods=['POST', 'GET'])
def day_view():
    day_number = int(request.args.get('dayNum', 1))
    tasks = db.get_tasks_for_day(day_number)
    return render_template('dayView.html', day_number=day_number, day_name='Logsday', month_name='October', military_time=False, tasks=tasks)

@app.route('/addTask', methods=['POST', 'GET'])
def add_event():
    return render_template('addTask.html', day_number=int(request.args['dayNum']), day_name='Logsday', month_name='October')

@app.route('/addTask/newTask', methods=['POST', 'GET'])
def receive_task():
    task_name = request.form["task_name"]
    from_time = int(request.form["from_time"])
    to_time = int(request.form["to_time"])
    day_number = int(request.args['dayNum'])
    
    task = {
        "title": task_name,
        "start_time": from_time,
        "duration": to_time - from_time,
        "day_number": day_number,
        "is_task": True
    }
    db.add_task(task)
    
    return redirect(url_for('index'))

@app.route('/viewTask', methods=['POST', 'GET'])
def view_task():
    task_id = request.args['taskId']
    task = db.get_task_by_id(ObjectId(task_id))
    return render_template('viewTask.html', task=task)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
