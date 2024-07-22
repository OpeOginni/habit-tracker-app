import os
import pytest
import tempfile
from flask import Flask
from db.db import SqliteDB
from routes.habits import load as load_habits

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    
    app = Flask(__name__)
    app.config.update({
        "TESTING": True,
        "DATABASE": os.getenv("DB_FILE_NAME")
    })

    # Load the schema and seed the database
    with app.app_context():
        with open(os.path.join(os.path.dirname(__file__), '../db/sql/schema.sql'), 'r') as f:
            SqliteDB().cursor.executescript(f.read())
        with open(os.path.join(os.path.dirname(__file__), '../db/sql/seed.sql'), 'r') as f:
            SqliteDB().cursor.executescript(f.read())

    # Load analytics routes
    load_habits(app)

    yield app

    # Clean up the database
    # os.unlink(app.config["DATABASE"])
    # os.remove(app.config["DATABASE"])

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

def test_get_habits(client):
    """Test fetching all habits."""
    response = client.get("/api/habits")
    assert response.status_code == 200
    data = response.get_json()
    assert 'habits' in data
    assert len(data['habits']) > 0

def test_get_habit(client):
    """Test fetching a specific habit by name."""
    response = client.get("/api/habits/Read")
    assert response.status_code == 200
    data = response.get_json()
    assert 'habit' in data
    assert data['habit']['name'] == 'Read'

def test_get_habit_not_found(client):
    """Test fetching a non-existent habit."""
    response = client.get("/api/habits/NonExistentHabit")
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data

def test_get_habit_by_periodicity(client):
    """Test fetching habits by periodicity."""
    response = client.get("/api/habits/periodicity/DAILY")
    assert response.status_code == 200
    data = response.get_json()
    assert 'habits' in data
    assert len(data['habits']) > 0

def test_create_new_habit(client):
    """Test creating a new habit."""
    response = client.post("/api/habits/create", json={
        'habit_name': 'TestHabit',
        'description': 'Daily workout',
        'periodicity': 'DAILY'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Habit Created'
    
def test_create_new_habit_with_already_existing_name(client):
    """Test creating a new habit."""
    response = client.post("/api/habits/create", json={
        'habit_name': 'Exercise',
        'description': 'Daily workout',
        'periodicity': 'DAILY'
    })
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Habit with the same name already exists'

def test_track_habit(client):
    """Test tracking a habit for a user."""
    response = client.post("/api/habits/track/Read", json={'username': 'testuser'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Started Tracking Habit'

def test_untrack_habit(client):
    """Test untracking a habit for a user."""
    client.post("/api/habits/track/Read", json={'username': 'testuser'})
    response = client.delete("/api/habits/untrack/Read", json={'username': 'testuser'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Habit Untracked'

def test_check_off_habit(client):
    """Test checking off a habit for a user."""
    client.post("/api/habits/track/Read", json={'username': 'testuser'})
    response = client.post("/api/habits/check-off/Read", json={'username': 'testuser'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Habit checked off'