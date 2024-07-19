import os
from dotenv import load_dotenv
import sqlite3

# Load environment variables from a .env file
load_dotenv()

def seedData():
    """
    Reads the SQL code for seeding the database from a file and runs it on the SQLite database.

    This function:
    - Reads the seed SQL file from the 'sql' directory.
    - Connects to the SQLite database using the file name specified in the .env file.
    - Executes the seed SQL script to populate the database with initial data.
    
    Raises:
    -------
    sqlite3.Error
        If an error occurs during the database connection or seed execution.
    """
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
    seed_file_path = os.path.join(__location__, 'sql', 'seed.sql')
    
    # Read the seed.sql file
    seed_str = open(seed_file_path).read()
    
    try:
        # Connect to SQLite DB
        DB_FILE_NAME = os.getenv("DB_FILE_NAME")
    
        sqliteConnection = sqlite3.connect(DB_FILE_NAME, check_same_thread=False)
    
        # Execute the seed script and load it in
        sqliteConnection.cursor().executescript(seed_str)
        sqliteConnection.commit()
    except sqlite3.Error as error:
        print('Error occurred - ', error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
    
    print('Seeding completed')

# Command to run this script -> python3 ./db/seed-db.py
seedData()