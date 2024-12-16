"""
Pytest test cases
"""

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
    task = {
        "title": "testing",
        "description": "testingDescription",
        "start_date": "2024-12-1",
        "day_number": 1,
        "is_task": False,
        "from_time": "1:00AM", # redundant, but used
        "to_time": "2:00AM", # redundant, but used
        "start_time_mfm": 60,
        "duration_minutes": 60,
    }
    response = client.post("/newEvent/create?dayNum=1", data=task)
    assert response.status_code == 302  # Redirect after creation
    assert "/dayView?dayNum=1" in response.headers["Location"]
