import datetime
from db.db import squlite_db

class Habit:
    def __init__(self, user_name):
        self.user_name = user_name
        self.db = squlite_db
        
    # GET GENERAL HABITS
    def get_all_habits(self):
        data = self.db.cursor().execute("SELECT * FROM public.habits")
        return data.fetchall()
    
    def get_habit(self, habit_name):
        data = self.db.cursor().execute("SELECT * FROM public.habits WHERE habit_name = ?", (habit_name))
        return data.fetchone()
    
    def get_habit_by_periodicity(self, periodicity):
        data = self.db.cursor().execute("SELECT * FROM public.habits WHERE periodicity = ?", (periodicity))
        return data.fetchall()
        
    # GET USER HABIT INFO
    def get_habit_current_streak(self, habit_name):
        data = self.db.cursor().execute("SELECT current_streak FROM public.user_habits WHERE habit_name = ?", (habit_name))
        return data.fetchone()
        
    def get_habit_longest_streak(self, habit_name):
        data = self.db.cursor().execute("SELECT longest_streak FROM public.user_habits WHERE habit_name = ?", (habit_name))
        return data.fetchone()
        
    # USER HABIT ACTIONS
    def start_habit(self, habit_name):
        _habit_id = self.db.cursor().execute("SELECT id FROM public.habits WHERE habit_name = ?", (habit_name))
        habit_id = _habit_id.fetchone()

        self.db.cursor().execute("INSERT INTO public.user_habits (habit_id, user_name) VALUES (?, ?)", (habit_id, self.user_name))
        
        self.db.commit()
        
    def delete_habit(self, habit_name):
        self.db.cursor().execute("DELETE FROM public.user_habits WHERE habit_name = ?", (habit_name))
        self.db.commit()
        
    def check_off_habit(self, habit_name):
        _user_habit_id = self.db.cursor().execute("SELECT id FROM public.user_habits WHERE habit_name = ? AND user_name = ?", (habit_name, self.user_name))
        user_habit_id = _user_habit_id.fetchone()
        
        # Track Habit
        self.__track_habit(user_habit_id)
        
        last_completed_date = self.__get_last_completed_habit_tracked_date(user_habit_id)
        periodicity = self.__get_habit_periodicity(habit_name)
        current_streak = self.get_habit_current_streak(habit_name)
        longest_streak = self.get_habit_longest_streak(habit_name)

        if last_completed_date:
            last_completed_date = last_completed_date[0]
            today = datetime.now().date()
            yesterday = today - datetime.timedelta(days=1)
            last_week = today - datetime.timedelta(days=7)

            if last_completed_date == datetime.now().date():
                return "Habit already checked off today"
            elif periodicity == 'DAILY' and last_completed_date == yesterday:
                self.__increment_habit_streak(habit_name)
    
            elif periodicity == 'WEEKLY' and (yesterday <= last_completed_date <= last_week):
                self.__increment_habit_streak(habit_name)
            else:
                self.__reset_habit_streak(habit_name)
        else:
            self.__increment_habit_streak(habit_name)

        if current_streak + 1 > longest_streak:
            self.__increment_longest_streak(habit_name)        
    
    # PRIVATE HABIT METHODS
    def __increment_habit_streak(self, habit_name):
        self.db.cursor().execute("UPDATE public.user_habits SET current_streak = current_streak + 1 WHERE habit_name = ? AND user_name = ?", (habit_name, self.user_name))
        self.db.commit()
        
    def __reset_habit_streak(self, habit_name):
        self.db.cursor().execute("UPDATE public.user_habits SET current_streak = 0 WHERE habit_name = ? AND user_name = ?", (habit_name, self.user_name))
        self.db.commit()
        
    def __increment_longest_streak(self, habit_name):
        self.db.cursor().execute("UPDATE public.user_habits SET longest_streak = current_streak + 1 WHERE habit_name = ? AND user_name = ?", (habit_name, self.user_name))
        self.db.commit()
        
    def __track_habit(self, user_habit_id):
        self.db.cursor().execute("INSERT INTO public.habit_tracking (user_habit_id) VALUES (?)", (user_habit_id))
        self.db.commit()
        
    def __get_last_completed_habit_tracked_date(self, user_habit_id):
        data = self.db.cursor().execute("SELECT completed_at FROM public.habit_tracking WHERE user_habit_id = ? ORDER BY completed_at DESC LIMIT 1", (user_habit_id))
        return data.fetchone()
    
    def __get_habit_periodicity(self, habit_id):
        data = self.db.cursor().execute("SELECT periodicity FROM public.habits WHERE habit_id = ?", (habit_id))
        return data.fetchone()