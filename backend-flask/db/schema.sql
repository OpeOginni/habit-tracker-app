DROP TABLE IF EXISTS public.habits;
DROP TABLE IF EXISTS public.user_habits;
DROP TABLE IF EXISTS public.habit_tracker;

CREATE TABLE public.habits (
    id INTEGER UNIQUE PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    periodicity VARCHAR(10) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
)

CREATE TABLE public.user_habits (
    id INTEGER UNIQUE PRIMARY KEY,
    habit_id INTEGER NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    current_streak INTEGER NOT NULL DEFAULT 0,
    longest_streak INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (habit_id) REFERENCES public.habits(id)
)

CREATE TABLE public.habit_tracker (
    id INTEGER UNIQUE PRIMARY KEY,
    user_habit_id INTEGER NOT NULL,
    completed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_habit_id) REFERENCES public.user_habits(id)
)