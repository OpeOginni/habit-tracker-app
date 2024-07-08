import os
import sqlite3
from flask import current_app as app

class SqliteDB:
    def __init__(self):
        self.init_pool()
    
    def init_pool(self):
        try:
            # Connect to DB and create a cursor
            connection_url = os.getenv("CONNECTION_URL")

            sqliteConnection = sqlite3.connect(connection_url)
            cursor = sqliteConnection.cursor()
            
            self.cursor = cursor        
        # Handle errors
        except sqlite3.Error as error:
            print('Error occurred - ', error)

squlite_db = SqliteDB()