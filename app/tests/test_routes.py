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
