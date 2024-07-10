import os
from dotenv import load_dotenv
import sqlite3

load_dotenv()

def loadSchema():
    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
    seed_file_path = os.path.join(__location__, 'sql', 'seed.sql')
    
    # Read the Schema.sql file
    seed_str = open(seed_file_path).read()
    
    try:
        # Connect to SQLite DB
        DB_FILE_NAME = os.getenv("DB_FILE_NAME")
    
        sqliteConnection = sqlite3.connect(DB_FILE_NAME, check_same_thread=False)
    
        # Execute the Schema and Load it in
        sqliteConnection.cursor().executescript(seed_str)
    except sqlite3.Error as error:
        print('Error occurred - ', error)
    
    print('Seeding completed')
loadSchema()

# python3 ./db/seed-db.py
