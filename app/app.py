from flask import Flask, render_template, request, redirect, url_for
import os
from bson.objectid import ObjectId
import db, util

app = Flask(__name__)

# Constants for paths
pathViewCalendar = "/" # view a month
pathViewDay = "/dayView" # view events for a day
pathViewTaskOrEvent = "/viewTaskEvent" # view an event/task (with possibility to delete)
pathNewEvent = "/newEvent" # screen for adding an event
pathCreateEvent = "/newEvent/create" # will actually put it in the database
pathDeleteTaskOrEvent = "/deleteTask" # delete a task/event
pathClearDatabase = "/clearDatabase" # DANGER: completely clear database | curl -X POST http://localhost/clearDatabase while app is running

@app.route(pathViewCalendar, methods=['POST', 'GET'])
def index():
    return render_template('calendar.html', first_day_offset=2, num_days=31, month_name='October', last_month_days=30,
                           pathViewDay=pathViewDay)

# helper route to clear the db during development
# use curl -X POST http://localhost/clearDatabase in console when app is running
@app.route(pathClearDatabase, methods=['POST'])
def clear_database():
    db.clear_db()
    return "Database cleared successfully!", 200

@app.route(pathViewDay, methods=['POST', 'GET'])
def day_view():
    day_number = int(request.args.get('dayNum', 1))
    tasks = db.get_tasks_for_day(day_number)
    return render_template('dayView.html', day_number=day_number, day_name='Tuesday', month_name='October', military_time=False, tasks=tasks,
                           pathNewEvent=pathNewEvent, pathViewTaskOrEvent=pathViewTaskOrEvent, pathViewCalendar=pathViewCalendar)

@app.route(pathNewEvent, methods=['POST', 'GET'])
def add_event():
    return render_template('addEvent.html', day_number=int(request.args['dayNum']), day_name='Tuesday', month_name='October', 
                           pathViewDay=pathViewDay, pathCreateEvent=pathCreateEvent)

@app.route(pathCreateEvent, methods=['POST', 'GET'])
def receive_event():
    name = request.form["event_name"]
    from_time = request.form["from_time"]
    to_time = request.form["to_time"]
    day_number = int(request.args['dayNum'])
    
    start_time = util.time_to_minutes(from_time)
    end_time = util.time_to_minutes(to_time)
    duration = end_time - start_time

    task = {
        "title": name,
        "from_time": from_time,
        "to_time": to_time,
        "start_time_mfm": start_time,
        "duration_minutes": duration,
        "day_number": day_number,
        "is_task": False # this is an event, not a task
    }
    db.add_task(task)
    
    return redirect(f"{pathViewDay}?dayNum={day_number}")

@app.route(pathViewTaskOrEvent, methods=['POST', 'GET'])
def view_task_event():
    task_id = request.args['taskId']
    task = db.get_task_by_id(ObjectId(task_id))
    return render_template('viewTaskEvent.html', task=task, 
                           pathViewDay=pathViewDay, pathViewCalendar=pathViewCalendar, pathDeleteTaskOrEvent=pathDeleteTaskOrEvent)


@app.route(pathDeleteTaskOrEvent, methods=['POST', 'GET'])
def delete_task():
    task_id = request.args.get('taskId', 1)
    task = db.get_task_by_id(ObjectId(task_id))
    day_number = int(task["day_number"])
    db.delete_task(task)
    return redirect(f"{pathViewDay}?dayNum={day_number}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
