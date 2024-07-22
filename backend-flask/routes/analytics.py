# flask
from db.db import squlite_db

def load(app):
    """
    Load the analytics routes into the given Flask application.

    Parameters:
    ----------
    app : Flask
        The Flask application instance where the routes will be registered.
    """
    
    @app.route("/api/analytics/habits/tracking/<string:user_name>", methods=["GET"])
    def get_user_tracked_habits(user_name):
        """
        Get all habits tracked by a specific user.

        Parameters:
        ----------
        user_name : str
            The name of the user.

        Returns:
        -------
        dict
            A dictionary containing the user's name and their tracked habits.
        int
            The HTTP status code.
        """
        data = squlite_db.cursor.execute("SELECT * FROM user_habits WHERE user_name = ?", (user_name,))
        return {'user': user_name, 'trackedHabits': data.fetchall()}, 200

    @app.route("/api/analytics/user/<string:user_name>/longest-streak", methods=["GET"])
    def get_all_user_habits_longest_streak(user_name):
        """
        Get the longest streak for all habits tracked by a specific user.

        Parameters:
        ----------
        user_name : str
            The name of the user.

        Returns:
        -------
        dict
            A dictionary containing the longest streaks of the user's habits.
        int
            The HTTP status code.
        """
        data = squlite_db.cursor.execute(
            """SELECT 
                   user_habits.user_name,
                   habits.name AS habit_name,
                   user_habits.longest_streak 
                FROM 
                   user_habits 
                JOIN 
                   habits ON user_habits.habit_id = habits.id
                WHERE 
                   user_name = ?""",
            (user_name,)
        )
        return {'data': data.fetchall()}, 200

    @app.route("/api/analytics/user/<string:user_name>/longest-streak/<string:habit_name>", methods=["GET"])
    def find_user_habit_longest_streak(user_name, habit_name):
        """
        Get the longest streak for a specific habit tracked by a specific user.

        Parameters:
        ----------
        user_name : str
            The name of the user.
        habit_name : str
            The name of the habit.

        Returns:
        -------
        dict
            A dictionary containing the longest streak of the specified habit.
        int
            The HTTP status code.
        """
        
        _habit_id = squlite_db.cursor.execute("SELECT id FROM habits WHERE name = ?", (habit_name,))
        habit = _habit_id.fetchone()
        if habit is None:
            return {'message': 'Habit not found'}, 404
        
        habit_id = habit['id']

        data = squlite_db.cursor.execute("SELECT longest_streak FROM user_habits WHERE user_name = ? AND habit_id = ?", (user_name, habit_id,))
        return {'data': data.fetchone()}, 200

    @app.route("/api/analytics/user/<string:user_name>/tracked-timestamps/<string:habit_name>", methods=["GET"])
    def get_all_habits_tracked_timestamps(user_name, habit_name):
        """
        Get all tracked timestamps for a specific habit tracked by a specific user.

        Parameters:
        ----------
        user_name : str
            The name of the user.
        habit_name : str
            The name of the habit.

        Returns:
        -------
        dict
            A dictionary containing the user's name, the habit, and the tracked timestamps.
        int
            The HTTP status code.
        """
        _habit_id = squlite_db.cursor.execute("SELECT id FROM habits WHERE name = ?", (habit_name,))
        habit = _habit_id.fetchone()
        if habit is None:
            return {'message': 'Habit not found'}, 404
        
        habit_id = habit['id']

        data = squlite_db.cursor.execute(
            """SELECT 
                   habit_tracker.completed_at
                FROM 
                   user_habits 
                JOIN 
                   habit_tracker ON user_habits.id = habit_tracker.user_habit_id
                WHERE 
                   user_name = ? AND habit_id = ?
                ORDER BY habit_tracker.completed_at DESC""",
            (user_name, habit_id,)
        )
        return {'data': {'user_name': user_name, 'habit': habit_name, 'timestamps': data.fetchall()}}, 200
