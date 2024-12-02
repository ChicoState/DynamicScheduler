from flask import Flask, render_template, request, redirect, url_for
import os
from bson.objectid import ObjectId
import db, util

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    military_time = False
    if (military_time):
        current_time = util.get_current_time_military()
    else: 
        current_time = util.get_current_time_12h()
    
    current_date = util.get_current_date()
    return render_template('calendar.html',
                           action_name='dayView', first_day_offset=2, num_days=31,
                           month_name='October', last_month_days=30,
                           current_time=current_time, current_date=current_date)

# helper route to clear the db during development
# use curl -X POST http://localhost/clearDatabase in console when app is running
@app.route('/clearDatabase', methods=['POST'])
def clear_database():
    db.clear_db()
    return "Database cleared successfully!", 200

@app.route('/dayView', methods=['POST', 'GET'])
def day_view():

        

    day_number = int(request.args.get('dayNum', 1))
    tasks = db.get_tasks_for_day(day_number)
    return render_template('dayView.html', day_number=day_number, day_name='Tuesday', month_name='October', military_time=False, tasks=tasks)

@app.route('/addTask', methods=['POST', 'GET'])
def add_event():
    return render_template('addTask.html', day_number=int(request.args['dayNum']), day_name='Tuesday', month_name='October')

@app.route('/addTask/newTask', methods=['POST', 'GET'])
def receive_task():
    task_name = request.form["task_name"]
    from_time = request.form["from_time"]
    to_time = request.form["to_time"]
    day_number = int(request.args['dayNum'])
    
    start_time = util.time_to_minutes(from_time)
    end_time = util.time_to_minutes(to_time)
    duration = end_time - start_time


    task = {
        "title": task_name,
        "from_time": from_time,
        "to_time": to_time,
        "start_time_mfm": start_time,
        "duration_minutes": duration,
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
    # vvv Below is Alex's code that does not pull from database (merge conflict with main, i decided to keep it here) vvv
    #task_id = request.args.get('taskId')  # Retrieved from query string (GET part)
    # day_name = request.form.get('day_name')  # Retrieved from form (POST part)
    # month_name = request.form.get('month_name')
    # day_number = request.form.get('day_number')
    # # Render the template with these values
    # return render_template('viewTask.html', 
    #                        action_name='dayView',
    #                        task_id=task_id, 
    #                        day_number=day_number, 
    #                        day_name=day_name , 
    #                        month_name=month_name,
    #                        military_time=False)


@app.route('/deleteTask', methods=['POST', 'GET'])
def deleteTask():
    task_id = request.args.get('taskId', 1)
    task = db.get_task_by_id(ObjectId(task_id))
    day_number = int(task["day_number"])
    db.delete_task(task)
    return redirect(f"/dayView?dayNum={day_number}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
