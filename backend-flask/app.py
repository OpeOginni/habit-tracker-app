from flask import Flask

import routes.habits
import routes.analytics

# Create Flask app
app = Flask(__name__)

# Pass the app to the habits and analytics app, to register their respective routes
routes.habits.load(app)
routes.analytics.load(app)

# Test route
@app.route('/')
def root():
    return {'author': 'Opeyemi Oginni', 'message': 'Welcome to Habit Tracker API'}

if __name__ == "__main__":
  app.run(debug=True)