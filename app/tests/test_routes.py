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

def test_time_from_string():
    """Test conversion of string times to minutes since midnight"""
    assert time_from_string("1pm") == 780  # Placeholder logic
    assert time_from_string("2pm") == 840  # Placeholder logic
    assert time_from_string("60") == 60  # Direct integer conversion

def test_string_from_time():
    """Test conversion of minutes since midnight to string times"""
    assert string_from_time(780) == "1pm"  # Placeholder logic
    assert string_from_time(840) == "2pm"  # Placeholder logic
    assert string_from_time(0) == "12am"  # Midnight
    assert string_from_time(720) == "12pm"  # Noon
    assert string_from_time(900) == "3pm"  # Afternoon

def test_time_to_minutes():
    """Test conversion of HH:MM string to minutes since midnight"""
    assert time_to_minutes("00:00") == 0  # Midnight
    assert time_to_minutes("12:00") == 720  # Noon
    assert time_to_minutes("23:59") == 1439  # One minute before midnight
    assert time_to_minutes("08:30") == 510  # Morning time

def test_get_current_time_12h():
    """Test retrieval of current time in 12-hour format"""
    # Calculate expected time in 12-hour format (PST)
    now = datetime.now()
    pst_now = now - timedelta(hours=8)
    expected_time = pst_now.strftime("%-I:%M %p")  # 12-hour format with AM/PM
    assert get_current_time_12h() == expected_time

def test_get_current_time_military():
    """Test retrieval of current time in 24-hour military format"""
    # Calculate expected time in military format (PST)
    now = datetime.now()
    pst_now = now - timedelta(hours=8)
    expected_time = pst_now.strftime("%H:%M")  # 24-hour format
    assert get_current_time_military() == expected_time

def test_get_current_time_mfm():
    """Test retrieval of current time in minutes from midnight (PST)"""
    # Calculate expected time in minutes from midnight (PST)
    now = datetime.now()
    pst_now = now - timedelta(hours=8)
    expected_minutes = pst_now.hour * 60 + pst_now.minute
    assert get_current_time_mfm() == expected_minutes

def test_get_current_date():
    """Test retrieval of the current date in Day/Month/Year format"""
    # Calculate expected date in PST
    now = datetime.now()
    pst_now = now - timedelta(hours=8)
    expected_date = pst_now.strftime("%d/%m/%Y")  # Day/Month/Year format
    assert get_current_date() == expected_date