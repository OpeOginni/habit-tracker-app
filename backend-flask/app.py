from flask import Flask

import routes.habits
import routes.analytics

app = Flask(__name__)

routes.habits.load(app)
routes.analytics.load(app)


@app.route('/')
def root():
    return {'author': 'Opeyemi Oginni', 'message': 'Welcome to Habit Tracker API'}

if __name__ == "__main__":
  app.run(debug=True)