from pymongo import MongoClient
import os

MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client.mydatabase
tasks_collection = db.tasks
tasks_collection.create_index("day_number")

def get_tasks_for_day(day_number):
    return list(tasks_collection.find({"day_number": day_number}))

def add_task(task):
    tasks_collection.insert_one(task)

def get_task_by_id(task_id):
    return tasks_collection.find_one({"_id": task_id})
