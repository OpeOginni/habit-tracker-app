import os
import sqlite3
from flask import current_app as app

class SqliteDB:
    def __init__(self):
        self.init_pool()
    
    # https://stackoverflow.com/a/68991192
    def __row_to_dict(self, cursor: sqlite3.Cursor, row: sqlite3.Row) -> dict:
      data = {}
      for idx, col in enumerate(cursor.description):
          data[col[0]] = row[idx]
      return data
    
    def init_pool(self):
        try:
            # Connect to DB and create a cursor
            DB_FILE_NAME = os.getenv("DB_FILE_NAME")

            conn = sqlite3.connect(DB_FILE_NAME, check_same_thread=False)
            conn.row_factory = self.__row_to_dict

            self.conn = conn
            self.cursor = conn.cursor()
        # Handle errors
        except sqlite3.Error as error:
            print('Error occurred - ', error)

squlite_db = SqliteDB()