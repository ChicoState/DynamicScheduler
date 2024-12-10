"""
WSGI File: Used by Gunicorn and Nginx
"""
from app import app

if __name__ == "__main__":
    app.run()
