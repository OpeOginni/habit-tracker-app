import os
from dotenv import load_dotenv
import sqlite3

# We need this requirement to be able to read the SQLite DB file name from our .env file
load_dotenv()

def loadSchema():
    """
    Reads the SQL code for the schema from a file and runs it on the SQLite database.

    This function:
    - Reads the schema SQL file from the 'sql' directory.
    - Connects to the SQLite database using the file name specified in the .env file.
    - Executes the schema SQL script to create the necessary tables and structure in the database.
    
    Raises:
    -------
    sqlite3.Error
        If an error occurs during the database connection or schema execution.
    """
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
    schema_file_path = os.path.join(__location__, 'sql', 'schema.sql')

    # Read the schema.sql file
    schema_str = open(schema_file_path).read()
    
    try:
        # Connect to SQLite DB
        DB_FILE_NAME = os.getenv("DB_FILE_NAME")
    
        sqliteConnection = sqlite3.connect(DB_FILE_NAME, check_same_thread=False)
    
        # Execute the schema and load it in
        sqliteConnection.cursor().executescript(schema_str)
        sqliteConnection.commit()
    except sqlite3.Error as error:
        print('Error occurred - ', error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
    
    print('Schema loaded')

# Command to run this script -> python3 ./db/load-schema.py
loadSchema()
