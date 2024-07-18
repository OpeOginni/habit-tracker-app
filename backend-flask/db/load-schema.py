import os
from dotenv import load_dotenv
import sqlite3

# We need this requiremnt to be able to read the SQLite DB File name from our .env file
load_dotenv()

# This Function Reads the SQL code for our Schema and runs it on our DB
def loadSchema():
    '''
    '''
    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
    schema_file_path = os.path.join(__location__, 'sql', 'schema.sql')

    # Read the Schema.sql file
    schema_str = open(schema_file_path).read()
    
    try:
        # Connect to SQLite DB
        DB_FILE_NAME = os.getenv("DB_FILE_NAME")
    
        sqliteConnection = sqlite3.connect(DB_FILE_NAME, check_same_thread=False)
    
        # Execute the Schema and Load it in
        sqliteConnection.cursor().executescript(schema_str)
    except sqlite3.Error as error:
        print('Error occurred - ', error)
    
    print('Schema loaded')
loadSchema()

# Command to Run this Script -> python3 ./db/load-schema.py