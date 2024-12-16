"""
Test config file
"""
import pytest
from app import app

@pytest.fixture
def client():
    """
    Pytest fixture to define the client
    """
    return app.test_client()
