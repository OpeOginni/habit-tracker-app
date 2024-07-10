# flask
from db.db import squlite_db

def load(app):
    @app.route("/api/analytics/habits/tracking/<string:user_name>", methods=["GET"])
    def get_user_tracked_habits(user_name):
        data = squlite_db.cursor().execute("SELECT * FROM user_habits WHERE user_name = ?", (user_name))
        return {'user': user_name, 'trackedHabits': data.fetchall()}, 200
        
    @app.route("/api/analytics/user/<string:user_name>/longest-streak", methods=["GET"])
    def get_all_user_habits_longest_streak(user_name):
        data = squlite_db.cursor().execute(
            """SELECT 
                   user_habits.user_name,
                   habits.name AS habit_name,
                   user_habits.longest_streak 
                FROM 
                   user_habits 
                JOIN 
                   habits ON user_habits.habit_id = habits.id
                WHERE 
                   user_name = ?"""
            , (user_name))
        return {'data': data.fetchall()}, 200
    
    @app.route("/api/analytics/user/<string:user_name>/longest-streak/<string:habit_name>", methods=["GET"])
    def find_user_habit_longest_streak(user_name, habit_name):
        data = squlite_db.cursor().execute("SELECT longest_streak FROM user_habits WHERE user_name = ? AND habit_name = ?", (user_name, habit_name))
        return {'data': data.fetchone()}, 200