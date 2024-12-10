"""
A file containing all database functions
"""
import os
from pymongo import MongoClient

MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client.mydatabase
tasks_collection = db.tasks
tasks_collection.create_index("day_number")

def get_tasks_for_day(day_number):
    """
    A function to get all tasks by day
    input: day_number -> int
    output: list_tasks -> list
    """
    return list(tasks_collection.find({"day_number": day_number}))

def add_task(task):
    """
    A function to add a task
    input: task -> int
    output: void
    """
    tasks_collection.insert_one(task)

def get_task_by_id(task_id):
    """
    A function to get tasks by id
    input: task_id -> int
    output: task
    """
    return tasks_collection.find_one({"_id": task_id})

def delete_task(task):
    """
    A function to delete a task
    input: task_id -> int
    output: void
    """
    tasks_collection.delete_one(task)

def clear_db():
    """
    A function to delete everything in the database: DANGER!
    input: void
    output: void
    """
    # Delete all documents in the collection
    tasks_collection.delete_many({})
