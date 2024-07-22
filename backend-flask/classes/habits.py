import datetime
from db.db import squlite_db

class Habit:
    """
    A class to represent a habit and handle all related queries and updates in the SQLite database.

    Attributes:
    ----------
    user_name : str
        Name of the user who owns the habit.

    Methods:
    -------
    get_all_habits():
        Fetches all habits from the database.
        
    get_habit(habit_name):
        Fetches a specific habit by name from the database.
        
    get_habit_by_periodicity(periodicity):
        Fetches habits based on their periodicity.
        
    create_habit(habit_name, description, periodicity):
        Creates a new habit in the database.
        
    get_habit_current_streak(habit_name):
        Gets the current streak for a user's specific habit.
        
    get_habit_longest_streak(habit_name):
        Gets the longest streak for a user's specific habit.
        
    track_habit(habit_name):
        Tracks a new habit for the user.
        
    untrack_habit(habit_name):
        Stops tracking a habit for the user.
        
    check_off_habit(habit_name):
        Checks off a habit as completed for the day/week.
        
    __increment_habit_streak(habit_name):
        Increments the current streak for a habit.
        
    __reset_habit_streak(habit_name):
        Resets the current streak for a habit.
        
    __increment_longest_streak(habit_name):
        Updates the longest streak for a habit if the current streak is longer.
        
    __get_last_completed_habit_tracked_date(user_habit_id):
        Fetches the last completed date for a tracked habit.
        
    __get_habit_periodicity(habit_id):
        Fetches the periodicity of a habit by its ID.
        
    __get_habit_id(habit_name):
        Fetches the ID of a habit by its name.
    """

    def __init__(self, user_name=None):
        """
        Initializes the Habit class with a user_name and sets up database connection tools.

        Parameters:
        ----------
        user_name : str, optional
            Name of the user who owns the habit.
        """
        self.user_name = user_name
        self.cur = squlite_db.cursor
        self.con = squlite_db.conn

    def get_all_habits(self):
        """
        Fetches all habits from the database.

        Returns:
        -------
        list
            A list of all habits.
        """
        data = self.cur.execute("SELECT * FROM habits")
        return data.fetchall()

    def get_habit(self, habit_name):
        """
        Fetches a specific habit by name from the database.

        Parameters:
        ----------
        habit_name : str
            The name of the habit to fetch.

        Returns:
        -------
        dict or tuple
            The habit details or an error message if not found.
        """
        data = self.cur.execute("SELECT * FROM habits WHERE name = ?", (habit_name,))
        habit = data.fetchone()
        if habit is None:
            return {"error": "Habit not found", "code": 404}
        return habit

    def get_habit_by_periodicity(self, periodicity):
        """
        Fetches habits based on their periodicity.

        Parameters:
        ----------
        periodicity : str
            The periodicity of the habits to fetch.

        Returns:
        -------
        list
            A list of habits with the specified periodicity.
        """
        data = self.cur.execute("SELECT * FROM habits WHERE periodicity = ?", (periodicity,))
        return data.fetchall()

    def create_habit(self, habit_name, description, periodicity):
        """
        Creates a new habit in the database.

        Parameters:
        ----------
        habit_name : str
            The name of the habit.
        description : str
            A description of the habit.
        periodicity : str
            The periodicity of the habit (e.g., 'DAILY', 'WEEKLY').

        Returns:
        -------
        dict
            A success message or an error message if the habit already exists.
        """
        data = self.cur.execute("SELECT * FROM habits WHERE name = ?", (habit_name,))
        habit = data.fetchone()
        if habit is not None:
            return {"error": "Habit with the same name already exists", "code": 400}
        
        self.cur.execute("INSERT INTO habits (name, description, periodicity) VALUES (?, ?, ?)", (habit_name, description, periodicity,))
        self.con.commit()
        
        return {"message": "Habit Created"}

    def get_habit_current_streak(self, habit_name):
        """
        Gets the current streak for a user's specific habit.

        Parameters:
        ----------
        habit_name : str
            The name of the habit.

        Returns:
        -------
        dict or tuple
            The current streak or an error message if user_name is not provided.
        """
        if self.user_name is None:
            return {"error": "user_name must be provided", "code": 400}

        _habit_id = self.__get_habit_id(habit_name)
        if _habit_id.get('error'):
            return _habit_id
        
        habit_id = _habit_id['id']
        

        data = self.cur.execute("SELECT current_streak FROM user_habits WHERE habit_id = ? AND user_name = ?", (habit_id, self.user_name,))
        return data.fetchone()

    def get_habit_longest_streak(self, habit_name):
        """
        Gets the longest streak for a user's specific habit.

        Parameters:
        ----------
        habit_name : str
            The name of the habit.

        Returns:
        -------
        dict or tuple
            The longest streak or an error message if user_name is not provided.
        """
        if self.user_name is None:
            return {"error": "user_name must be provided", "code": 400}
        _habit_id = self.__get_habit_id(habit_name)
        if _habit_id.get('error'):
            return _habit_id
        
        habit_id = _habit_id['id']
        
        data = self.cur.execute("SELECT longest_streak FROM user_habits WHERE habit_id = ? AND user_name = ?", (habit_id, self.user_name,))
        return data.fetchone()

    def track_habit(self, habit_name):
        """
        Tracks a new habit for the user.

        Parameters:
        ----------
        habit_name : str
            The name of the habit to track.

        Returns:
        -------
        dict
            A success message or an error message if user_name is not provided.
        """
        if self.user_name is None:
            return {"error": "user_name must be provided", "code": 400}
        _habit_id = self.__get_habit_id(habit_name)
        if _habit_id.get('error'):
            return _habit_id
        
        habit_id = _habit_id['id']
        
        user_tracked_habit_id = self.__get_user_tracked_habit_id(habit_id)
        
        if user_tracked_habit_id.get('error'):
            self.cur.execute("INSERT INTO user_habits (habit_id, user_name) VALUES (?, ?)", (habit_id, self.user_name,))
            self.con.commit()
            return {"message": "Started Tracking Habit"}
        else:
            return {"error": "User is already tracking this habit", "code": 400}
        

    def untrack_habit(self, habit_name):
        """
        Stops tracking a habit for the user.

        Parameters:
        ----------
        habit_name : str
            The name of the habit to stop tracking.

        Returns:
        -------
        dict
            A success message or an error message if user_name is not provided.
        """
        if self.user_name is None:
            return {"error": "user_name must be provided", "code": 400}
        _habit_id = self.__get_habit_id(habit_name)
        if _habit_id.get('error'):
            return _habit_id
        
        habit_id = _habit_id['id']
        
        user_tracked_habit_id = self.__get_user_tracked_habit_id(habit_id)
        
        if user_tracked_habit_id.get('error'):
            return user_tracked_habit_id

        self.cur.execute("DELETE FROM user_habits WHERE habit_id = ? AND user_name = ?", (habit_id, self.user_name,))
        self.con.commit()

    def check_off_habit(self, habit_name):
        """
        Checks off a habit as completed for the day/week.

        Parameters:
        ----------
        habit_name : str
            The name of the habit to check off.

        Returns:
        -------
        dict
            A success message or an error message if user_name is not provided or habit is already checked off for the period.
        """
        if self.user_name is None:
            return {"error": "user_name must be provided", "code": 400}
        _habit_id = self.__get_habit_id(habit_name)
        if _habit_id.get('error'):
            return _habit_id
        
        habit_id = _habit_id['id']
        
        user_tracked_habit_id = self.__get_user_tracked_habit_id(habit_id)
        
        if user_tracked_habit_id.get('error'):
            return user_tracked_habit_id

        # Track Habit
        self.track_habit(user_tracked_habit_id['id'])

        last_completed_date = self.__get_last_completed_habit_tracked_date(user_tracked_habit_id['id'])
        periodicity = self.__get_habit_periodicity(habit_id)
        current_streak = self.get_habit_current_streak(habit_name)
        longest_streak = self.get_habit_longest_streak(habit_name)

        if last_completed_date:
            last_completed_date = last_completed_date[0]
            today = datetime.date.today()
            yesterday = today - datetime.timedelta(days=1)
            last_week = today - datetime.timedelta(days=7)

            if last_completed_date == today:
                return {"error": "Habit already checked off today", "code": 400}
            elif periodicity == 'DAILY' and last_completed_date == yesterday:
                self.__increment_habit_streak(habit_name)
            elif periodicity == 'WEEKLY' and last_week <= last_completed_date <= yesterday:
                self.__increment_habit_streak(habit_name)
            else:
                self.__reset_habit_streak(habit_name)
        else:
            self.__increment_habit_streak(habit_name)

        if current_streak[0] + 1 > longest_streak[0]:
            self.__increment_longest_streak(habit_name)

    def __increment_habit_streak(self, habit_name):
        """
        Increments the current streak for a habit.

        Parameters:
        ----------
        habit_name : str
            The name of the habit.

        Returns:
        -------
        dict
            A success message or an error message if user_name is not provided.
        """
        if self.user_name is None:
            return {"error": "user_name must be provided", "code": 400}

        _habit_id = self.__get_habit_id(habit_name)
        if _habit_id.get('error'):
            return _habit_id
        
        habit_id = _habit_id['id']
        
        self.cur.execute("UPDATE user_habits SET current_streak = current_streak + 1 WHERE habit_id = ? AND user_name = ?", (habit_id, self.user_name,))
        self.con.commit()

    def __reset_habit_streak(self, habit_name):
        """
        Resets the current streak for a habit.

        Parameters:
        ----------
        habit_name : str
            The name of the habit.

        Returns:
        -------
        dict
            A success message or an error message if user_name is not provided.
        """
        if self.user_name is None:
            return {"error": "user_name must be provided", "code": 400}
        _habit_id = self.__get_habit_id(habit_name)
        if _habit_id.get('error'):
            return _habit_id
        
        habit_id = _habit_id['id']
        
        self.cur.execute("UPDATE user_habits SET current_streak = 0 WHERE habit_id = ? AND user_name = ?", (habit_id, self.user_name,))
        self.con.commit()

    def __increment_longest_streak(self, habit_name):
        """
        Updates the longest streak for a habit if the current streak is longer.

        Parameters:
        ----------
        habit_name : str
            The name of the habit.

        Returns:
        -------
        dict
            A success message or an error message if user_name is not provided.
        """
        if self.user_name is None:
            return {"error": "user_name must be provided", "code": 400}
        _habit_id = self.__get_habit_id(habit_name)
        if _habit_id.get('error'):
            return _habit_id
        
        habit_id = _habit_id['id']
        
        self.cur.execute("UPDATE user_habits SET longest_streak = current_streak WHERE habit_id = ? AND user_name = ?", (habit_id, self.user_name,))
        self.con.commit()

    def __get_last_completed_habit_tracked_date(self, user_habit_id):
        """
        Fetches the last completed date for a tracked habit.

        Parameters:
        ----------
        user_habit_id : int
            The ID of the user's tracked habit.

        Returns:
        -------
        dict or tuple
            The last completed date or an error message if not found.
        """
        data = self.cur.execute("SELECT completed_at FROM habit_tracker WHERE user_habit_id = ? ORDER BY completed_at DESC LIMIT 1", (user_habit_id,))
        habit = data.fetchone()
        if habit is None:
            return {"error": "Habit not found", "code": 404}

        return habit['completed_at']

    def __get_habit_periodicity(self, habit_id):
        """
        Fetches the periodicity of a habit by its ID.

        Parameters:
        ----------
        habit_id : int
            The ID of the habit.

        Returns:
        -------
        dict or tuple
            The periodicity of the habit or an error message if not found.
        """
        data = self.cur.execute("SELECT periodicity FROM habits WHERE id = ?", (habit_id,))
        habit = data.fetchone()
        if habit is None:
            return {"error": "Habit not found", "code": 404}
        return habit['periodicity']

    def __get_habit_id(self, habit_name):
        """
        Fetches the ID of a habit by its name.

        Parameters:
        ----------
        habit_name : str
            The name of the habit.

        Returns:
        -------
        dict or tuple
            The ID of the habit or an error message if not found.
        """
        data = self.cur.execute("SELECT id FROM habits WHERE name = ?", (habit_name,))
        habit = data.fetchone()
        if habit is None:
            return {"error": "Habit not found", "code": 404}
        return habit
    
    def __get_user_tracked_habit_id(self, habit_id):
        data = self.cur.execute("SELECT id FROM user_habits WHERE user_name = ? AND habit_id = ?", (self.user_name, habit_id,))
        user_habit = data.fetchone()
        if user_habit is None:
            return {"error": "Habit Not Tracked By User", "code": 404}
        return user_habit
