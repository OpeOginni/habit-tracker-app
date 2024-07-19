# flask
from flask import request, g
from flask_cors import cross_origin

# class
from classes.habits import Habit

def load(app):
    """
    Load the habit-related routes into the given Flask application.

    Parameters:
    ----------
    app : Flask
        The Flask application instance where the routes will be registered.
    """
    
    @app.route("/api/habits", methods=["GET"])
    def get_habits():
        """
        Get all habits.

        Returns:
        -------
        dict
            A dictionary containing all habits.
        int
            The HTTP status code.
        """
        habit = Habit()
        habits = habit.get_all_habits()
        return {'habits': habits}, 200

    @app.route("/api/habits/<string:habit_name>", methods=["GET"])
    def get_habit(habit_name):
        """
        Get a specific habit by name.

        Parameters:
        ----------
        habit_name : str
            The name of the habit.

        Returns:
        -------
        dict
            A dictionary containing the habit data or an error message.
        int
            The HTTP status code.
        """
        habit = Habit()
        habit_data = habit.get_habit(habit_name)
        if habit_data['error'] is not None:
            return {'error': habit_data['error']}, habit_data['code']
        return {'habit': habit_data}, 200

    @app.route("/api/habits/periodicity/<string:periodicity>", methods=["GET"])
    def get_habit_by_periodicity(periodicity):
        """
        Get habits by periodicity.

        Parameters:
        ----------
        periodicity : str
            The periodicity of the habits (e.g., DAILY, WEEKLY).

        Returns:
        -------
        dict
            A dictionary containing the habits with the specified periodicity.
        int
            The HTTP status code.
        """
        habit = Habit()
        habits = habit.get_habit_by_periodicity(periodicity)
        return {'habits': habits}, 200

    @app.route("/api/habits/create", methods=["POST"])
    def createNewHabit():
        """
        Create a new habit.

        Returns:
        -------
        dict
            A success message.
        int
            The HTTP status code.
        """
        habit_name = request.json.get('habit_name', None)
        description = request.json.get('description', None)
        periodicity = request.json.get('periodicity', None)

        habit = Habit()
        habit.create_habit(habit_name, description, periodicity)
        return {'message': 'Habit Created'}, 201

    @app.route("/api/habits/track/<string:habit_name>", methods=["POST"])
    def track_habit(habit_name):
        """
        Start tracking a habit for a user.

        Parameters:
        ----------
        habit_name : str
            The name of the habit.

        Returns:
        -------
        dict
            A success message or an error message if the user name is not provided.
        int
            The HTTP status code.
        """
        user_name = request.json.get('username', None)
        if user_name is None:
            return {'message': 'User name is required'}, 400
        
        habit = Habit(user_name)
        habit.track_habit(habit_name)
        return {'message': 'Started Tracking Habit'}, 200

    @app.route("/api/habits/untrack/<string:habit_name>", methods=["DELETE"])
    def untrack_habit(habit_name):
        """
        Stop tracking a habit for a user.

        Parameters:
        ----------
        habit_name : str
            The name of the habit.

        Returns:
        -------
        dict
            A success message or an error message if the user name is not provided.
        int
            The HTTP status code.
        """
        user_name = request.json.get('username', None)
        if user_name is None:
            return {'message': 'User name is required'}, 400

        habit = Habit(user_name)
        habit.untrack_habit(habit_name)
        return {'message': 'Habit Untracked'}, 200

    @app.route("/api/habits/check-off/<string:habit_name>", methods=["POST"])
    def check_off_habit(habit_name):
        """
        Check off a habit for a user.

        Parameters:
        ----------
        habit_name : str
            The name of the habit.

        Returns:
        -------
        dict
            A success message or an error message if the user name is not provided.
        int
            The HTTP status code.
        """
        user_name = request.json.get('username', None)
        if user_name is None:
            return {'message': 'User name is required'}, 400
        
        habit = Habit(user_name)
        habit.check_off_habit(habit_name)
        return {'message': 'Habit checked off'}, 200

    @app.route("/api/habits/user/<string:user_name>/streaks/<string:habit_name>", methods=["GET"])
    def get_user_streaks(user_name, habit_name):
        """
        Get the current and longest streaks for a specific habit tracked by a user.

        Parameters:
        ----------
        user_name : str
            The name of the user.
        habit_name : str
            The name of the habit.

        Returns:
        -------
        dict
            A dictionary containing the current and longest streaks for the specified habit.
        int
            The HTTP status code.
        """
        if user_name is None:
            return {'message': 'User name is required'}, 400
        
        habit = Habit(user_name)
        current_streak_data = habit.get_habit_current_streak(habit_name)
        longest_streak_data = habit.get_habit_longest_streak(habit_name)
        return {'habit_name': habit_name,
                'user_name': user_name,
                'currentStreak': current_streak_data['current_streak'],
                'longestStreak': longest_streak_data['longest_streak']
                }, 200
