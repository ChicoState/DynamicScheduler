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
    day_number = int(request.args.get('dayNum', 1))
    tasks = db.get_tasks_for_day(day_number)
    return render_template('dayView.html', day_number=day_number, day_name='Tuesday', month_name='October', military_time=False, tasks=tasks,
                            pathNewEvent=util.formatURI(pathNewEvent, dayNum=day_number),
                            pathRawViewTaskOrEvent=pathViewTaskOrEvent,
                            pathViewCalendar=pathViewCalendar)

@app.route(pathNewEvent, methods=['POST', 'GET'])
def add_event():
    day_number=int(request.args['dayNum'])
    return render_template('addEvent.html', day_number=day_number, day_name='Tuesday', month_number=12, month_name='December', year=2024,
                           pathViewDay=util.formatURI(pathViewDay, dayNum=day_number), 
                           pathCreateEvent=util.formatURI(pathCreateEvent, dayNum=day_number))


@app.route(pathCreateEvent, methods=['POST', 'GET'])
def receive_event():
    day_number=int(request.args['dayNum']) # is redundant, since we have 'start_date', but somebody didn't write a python util function to parse date into day, month, year

    name = request.form["event_name"]
    description = request.form["event_description"]
    start_date = request.form["start_date"]
    is_task = request.form["is_task"] == "true"
    if is_task:
        due_date = request.form["due_date"]
        duration = int(request.form["duration"])
        try:
            _ = request.form["can_split"]
            can_split = True
        except:
            can_split = False
    else:
        from_time = request.form["from_time"]
        to_time = request.form["to_time"]
    
        start_time = util.time_to_minutes(from_time)
        end_time = util.time_to_minutes(to_time)
        duration = end_time - start_time

    # testing the inputs vvv
    # if is_task:
    #     return render_template('debug.html', 
    #                        display=f"task: name={name}; desc={description}; sdate={start_date}; task={is_task}; can_split={can_split}; duration={duration}")
    # else:
    #     return render_template('debug.html', 
    #                        display=f"event: name={name}; desc={description}; sdate={start_date}; task={is_task}; from_time={from_time}; duration={duration}")
    
    if is_task:
        # is a task
        task = {
            "title": name,
            "description": description,
            "start_date": start_date,
            "from_time": from_time,
            "day_number": day_number,
            "is_task": True,
            "due_date": due_date,
            "duration_minutes": duration,
            "can_split": can_split,
        }
    else:
        # an event
        task = {
            "title": name,
            "description": description,
            "start_date": start_date,
            "from_time": from_time,
            "day_number": day_number,
            "is_task": True,
            "from_time": from_time, # redundant, but used
            "to_time": to_time, # redundant, but used
            "start_time_mfm": start_time,
            "duration_minutes": duration,
        }

    db.add_task(task)
    
    return redirect(util.formatURI(pathViewDay, dayNum=day_number))

@app.route(pathViewTaskOrEvent, methods=['POST', 'GET'])
def view_task_event():
    """A function to get tasks by objectid and render template"""
    task_id = request.args['taskId']
    task = db.get_task_by_id(ObjectId(task_id))
    return render_template('viewTaskEvent.html', task=task, 
                           pathBack=util.formatURI(pathViewDay, dayNum=task["day_number"]),
                           pathViewCalendar=pathViewCalendar, 
                           pathDeleteTaskOrEvent=util.formatURI(pathDeleteTaskOrEvent, taskId=task["_id"]))

@app.route(pathDeleteTaskOrEvent, methods=['POST', 'GET'])
def delete_task():
    """A function used to delete a task"""
    task_id = request.args.get('taskId', 1)
    task = db.get_task_by_id(ObjectId(task_id))
    day_number = int(task["day_number"])
    db.delete_task(task)
    return redirect(util.formatURI(pathViewDay, dayNum=day_number))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
