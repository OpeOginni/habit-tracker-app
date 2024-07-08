from db.db import squlite_db

class Habit:
    def __init__(self, user_name):
        self.user_name = user_name
        
    def get_habit_current_streak(self, habit_name):
        
    def get_habit_longest_streak(self, habit_name):
        
    # You search for a Habit in the habit table
    # Using the details of that Habit create a Habit for that User
    def start_habit(self, habit_name):

    def delete_habit(self, habit_name):
        
    def check_off_habit(self, habit_name):
        
    def __increment_habit_streak(self, habit_name):
        
    def __reset_habit_streak(self, habit_name):