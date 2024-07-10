DROP TABLE IF EXISTS habits;
DROP TABLE IF EXISTS user_habits;
DROP TABLE IF EXISTS habit_tracker;

CREATE TABLE habits (
    id INTEGER UNIQUE PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    periodicity VARCHAR(10) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_habits (
    id INTEGER UNIQUE PRIMARY KEY,
    habit_id INTEGER NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    current_streak INTEGER NOT NULL DEFAULT 0,
    longest_streak INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (habit_id) REFERENCES habits(id)
);

CREATE TABLE habit_tracker (
    id INTEGER UNIQUE PRIMARY KEY,
    user_habit_id INTEGER NOT NULL,
    completed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_habit_id) REFERENCES user_habits(id)
);