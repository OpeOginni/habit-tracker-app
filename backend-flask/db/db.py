import os
import sqlite3
from flask import current_app as app

# This is the SQLite Connection Class. 
# From this class, all parts of the app can have access to the Database.
class SqliteDB:
    def __init__(self, testDB=None):
        """
        Initialize the SqliteDB class and set up the connection pool.
        """
        self.testDB = testDB
        self.init_pool()
    
    def __row_to_dict(self, cursor: sqlite3.Cursor, row: sqlite3.Row) -> dict:
        """
        Convert a SQLite row object to a dictionary.

        Parameters:
        ----------
        cursor : sqlite3.Cursor
            The SQLite cursor object.
        row : sqlite3.Row
            The SQLite row object.

        Returns:
        -------
        dict
            A dictionary representing the row data.
        """
        data = {}
        for idx, col in enumerate(cursor.description):
            data[col[0]] = row[idx]
        return data
    
    def init_pool(self):
        """
        Initialize the connection pool by connecting to the SQLite database 
        and setting the row factory to return rows as dictionaries.
        """
        try:
            # Connect to DB and create a cursor
            
            conn = sqlite3.connect(os.getenv("DB_FILE_NAME"), check_same_thread=False)
            conn.row_factory = self.__row_to_dict

            self.conn = conn
            self.cursor = conn.cursor()
        # Handle error
        except sqlite3.Error as error:
            print('Error occurred - ', error)

# Global instance of the SqliteDB class
squlite_db = SqliteDB()
