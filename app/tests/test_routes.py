"""
Pytest test cases
"""
from datetime import datetime, timedelta
from util import time_from_string, string_from_time, time_to_minutes, get_current_time_12h, get_current_time_military, get_current_time_mfm, get_current_date

def test_index_route(client):
    """Test the index route"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"<html" in response.data

def test_day_view_route(client):
    """Test day view route"""
    response = client.get("/dayView?dayNum=1")
    assert response.status_code == 200
    assert b"<html" in response.data

def test_add_event_route(client):
    """Test the add event route"""
    response = client.get("/newEvent?dayNum=1")
    assert response.status_code == 200
    assert b"<html" in response.data

def test_clear_database(client):
    """Test the clear database route"""
    response = client.post("/clearDatabase")
    assert response.status_code == 200
    assert b"Database cleared successfully!" in response.data

def test_create_event_route(client):
    """Test the create event route"""
    response = client.post("/newEvent/create?dayNum=1", data={
        "event_name": "Meeting",
        "from_time": "10:00",
        "to_time": "11:00"
    })
    assert response.status_code == 302  # Redirect after creation
    assert "/dayView?dayNum=1" in response.headers["Location"]