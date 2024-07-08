from flask import Flask

app = Flask(__name__)

@app.route('/')
def root():
    return {'author': 'Opeyemi Oginni', 'message': 'Welcome to Habit Tracker API'}