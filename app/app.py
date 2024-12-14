"""
Dynamic Scheduler main flask instance
"""
import csv
import db
import util
from flask import Flask, render_template, request, redirect, session
from bson.objectid import ObjectId

app = Flask(__name__)

# Hello

# Constants for paths
pathViewCalendar = "/"  # view a month
pathViewDay = "/dayView"  # view events for a day
pathViewTaskOrEvent = "/viewTaskEvent"  # view an event/task (with possibility to delete)
pathNewEvent = "/newEvent"  # screen for adding an event
pathCreateEvent = "/newEvent/create"  # will actually put it in the database
pathDeleteTaskOrEvent = "/deleteTask"  # delete a task/event
pathClearDatabase = "/clearDatabase"
# DANGER: completely clear database
# curl -X POST http://localhost/clearDatabase
# while app is running
app.config['SECRET_KEY'] = 'csci430csci430csci430csci430csci430csci430csci430csci430'

@app.route(pathViewCalendar, methods=['POST', 'GET'])
def index():
    """
    Index of the site
    """
    military_time = False
    if military_time:
        current_time = util.get_current_time_military()
    else:
        current_time = util.get_current_time_12h()
    current_date = util.get_current_date()
    return render_template('calendar.html',
                           action_name='dayView', first_day_offset=2,
                           num_days=31, month_name='October', last_month_days=30,
                           current_time=current_time, current_date=current_date,
                           pathViewDay=pathViewDay)

@app.route(pathClearDatabase, methods=['POST'])
def clear_database():
    """A helper function used to clear the database
    """
    db.clear_db()
    return "Database cleared successfully!", 200

def load_users_from_csv():
    """Load usernames from a CSV file."""
    users = []
    with open('users/users.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            users.append(row[0])
    return users

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if request.method == 'POST':
        username = request.form['username']
        users = load_users_from_csv()
        if username in users:
            session['logged_in'] = True
            session['username'] = username
            return redirect(pathViewCalendar)
        return render_template('login.html', error='Invalid username')
    return render_template('login.html')

@app.route(pathViewDay, methods=['POST', 'GET'])
def day_view():
    """A route used for day view, the home page of the site"""
    day_number = int(request.args.get('dayNum', 1))
    tasks = db.get_tasks_for_day(day_number)
    return render_template('dayView.html', day_number=day_number,
                           day_name='Tuesday', month_name='December',
                           military_time=False, tasks=tasks,
                           pathNewEvent=pathNewEvent, pathViewTaskOrEvent=pathViewTaskOrEvent,
                           pathViewCalendar=pathViewCalendar)

@app.route(pathNewEvent, methods=['POST', 'GET'])
def add_event():
    """A route used to add an event"""
    return render_template('addEvent.html', day_number=int(request.args['dayNum']),
                           day_name='Tuesday', month_name='December',
                           pathViewDay=pathViewDay, pathCreateEvent=pathCreateEvent)

@app.route(pathCreateEvent, methods=['POST', 'GET'])
def receive_event():
    """A request form used to add an event/task"""
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
        "is_task": False
    }
    db.add_task(task)

    return redirect(f"{pathViewDay}?dayNum={day_number}")

@app.route(pathViewTaskOrEvent, methods=['POST', 'GET'])
def view_task_event():
    """A function to get tasks by objectid and render template"""
    task_id = request.args['taskId']
    task = db.get_task_by_id(ObjectId(task_id))
    return render_template('viewTaskEvent.html', task=task,
                           pathViewDay=pathViewDay, pathViewCalendar=pathViewCalendar,
                           pathDeleteTaskOrEvent=pathDeleteTaskOrEvent)

@app.route(pathDeleteTaskOrEvent, methods=['POST', 'GET'])
def delete_task():
    """A function used to delete a task"""
    task_id = request.args.get('taskId', 1)
    task = db.get_task_by_id(ObjectId(task_id))
    day_number = int(task["day_number"])
    db.delete_task(task)
    return redirect(f"{pathViewDay}?dayNum={day_number}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
