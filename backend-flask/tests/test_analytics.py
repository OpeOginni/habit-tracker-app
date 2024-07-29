import os
import pytest
import tempfile
from flask import Flask
from db.db import SqliteDB
from routes.analytics import load as load_analytics
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
    load_analytics(app)
    load_habits(app)

    yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

def test_get_user_tracked_habits(client):
    """Test fetching all tracked habits for a user."""
    response = client.get("/api/analytics/habits/tracking/Alice")
    assert response.status_code == 200
    data = response.get_json()
    assert 'trackedHabits' in data
    assert len(data['trackedHabits']) > 0

def test_get_all_user_habits_longest_streak(client):
    """Test fetching the longest streak for all habits of a user."""
    response = client.get("/api/analytics/user/Alice/longest-streak")
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert len(data['data']) > 0

def test_find_user_habit_longest_streak(client):
    """Test fetching the longest streak for a specific habit of a user."""
    response = client.get("/api/analytics/user/Alice/longest-streak/Read")
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert 'longest_streak' in data['data']
    assert data['data']['longest_streak'] == 8 # Alice's longest streak for the 'Read' habit according to the seed data
    
def test_get_user_habit_current_streak_after_check_off(client):
    """Test fetching the current streak for a habit after checking it off."""
    response = client.post("/api/habits/check-off/Read", json={'username': 'Alice'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'Habit checked off'

    response = client.get("/api/habits/user/Alice/streaks/Read")
    assert response.status_code == 200
    data = response.get_json()
    assert 'current_streak' in data
    assert data['current_streak'] == 1

def test_get_all_habits_tracked_timestamps(client):
    """Test fetching all timestamps for tracked habits of a user."""
    response = client.get("/api/analytics/user/Alice/tracked-timestamps/Read")
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert 'timestamps' in data['data']
    assert len(data['data']['timestamps']) > 0

def test_get_user_tracked_habits_no_user(client):
    """Test fetching tracked habits for a non-existent user."""
    response = client.get("/api/analytics/habits/tracking/nonexistentuser")
    assert response.status_code == 200
    data = response.get_json()
    assert 'trackedHabits' in data
    assert len(data['trackedHabits']) == 0

def test_find_user_habit_longest_streak_no_habit(client):
    """Test fetching the longest streak for a non-existent habit."""
    response = client.get("/api/analytics/user/Alice/longest-streak/NonExistentHabit")
    assert response.status_code == 404
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'Habit not found'

def test_get_all_habits_tracked_timestamps_no_habit(client):
    """Test fetching timestamps for a non-existent habit."""
    response = client.get("/api/analytics/user/Alice/tracked-timestamps/NonExistentHabit")
    assert response.status_code == 404
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'Habit not found'
