# flask
from flask import request, g
from flask_cors import cross_origin

# class
from classes.habits import Habit

def load(app):
    @app.route("/api/habits", methods=["GET"])
    def get_habits():
        habit = Habit('')
        habits = habit.get_all_habits()
        return {'habits': habits}, 200
    
    @app.route("/api/habits/<string:habit_name>", methods=["GET"])
    def get_habit(habit_name):
        habit = Habit('')
        habit_data = habit.get_habit(habit_name)
        return {'habit': habit_data}, 200
    
    @app.route("/api/habits/periodicity/<string:periodicity>", methods=["GET"])
    def get_habit_by_periodicity(periodicity):
        habit = Habit('')
        habits = habit.get_habit_by_periodicity(periodicity)
        return {'habits': habits}, 200
    
    @app.route("/api/habits/start/<string:habit_name>", methods=["POST"])
    def start_habit(habit_name):
        user_name = request.json.get('userName', None)
        if user_name is None:
            return {'message': 'User name is required'}, 400
        
        habit = Habit(user_name)
        habit.start_habit(habit_name)
        return {'message': 'Habit started'}, 200
    
    @app.route("/api/habits/delete/<string:habit_name>", methods=["DELETE"])
    def delete_habit(habit_name):
        user_name = request.json.get('userName', None)
        if user_name is None:
            return {'message': 'User name is required'}, 400

        habit = Habit(user_name)
        habit.delete_habit(habit_name)
        return {'message': 'Habit deleted'}, 200
    
    @app.route("/api/habits/check-off/<string:habit_name>", methods=["POST"])
    def check_off_habit(habit_name):
        user_name = request.json.get('userName', None)
        if user_name is None:
            return {'message': 'User name is required'}, 400
        
        habit = Habit(user_name)
        habit.check_off_habit(habit_name)
        return {'message': 'Habit checked off'}, 200
    
    @app.route("/api/habits/streaks/<string:habit_name>", methods=["GET"])
    def get_user_streaks(habit_name):
        user_name = request.json.get('userName', None)
        if user_name is None:
            return {'message': 'User name is required'}, 400
        
        habit = Habit(user_name)
        current_streak = habit.get_habit_current_streak(habit_name)
        longest_streak = habit.get_habit_longest_streak(habit_name)
        return {'habit_name': habit_name, 'currentStreak': current_streak, 'longestStreak': longest_streak}, 200