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
    taskRaw = {'event_name': 'testing',
            'event_description': 'testingDescription',
            'start_date': '2024-12-01',
            'is_task': 'false',
            'from_time': '10:00',
            'to_time': '13:00'
            }
    response = client.post("/newEvent/create?dayNum=1", data=taskRaw)
    assert response.status_code == 302  # Redirect after creation
    assert "/dayView?dayNum=1" in response.headers["Location"]
