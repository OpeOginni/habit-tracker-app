-- Seeding Habits

INSERT INTO
    habits (name, description, periodicity)
VALUES
    ('Read', 'Spend some time reading a book everyday', 'DAILY'),
    ('Exercise', 'Engage in physical activity to stay healthy', 'WEEKLY'),
    ('Park Walk', 'Get some Sun on the Skin', 'WEEKLY'),
    ('Meditate', 'Practice meditation to improve mindfulness', 'DAILY'),
    ('Journal', 'Write in a journal to reflect on your day', 'DAILY');

-- Seeding User Habits

INSERT INTO
    user_habits (habit_id, user_name, current_streak, longest_streak)
VALUES
    (1, 'Alice', 4, 8),
    (2, 'Alice', 3, 3),
    (2, 'Bob', 5, 5),
    (3, 'Bob', 3, 2),
    (5, 'Bob', 0, 1);

