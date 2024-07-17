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

-- Seeding Habit Tracker

-- Alice's "Read" habit (current streak 4, longest streak 8)
-- Current streak
INSERT INTO habit_tracker (user_habit_id, completed_at) VALUES 
(1, '2024-07-13 09:00:00'),
(1, '2024-07-12 09:00:00'),
(1, '2024-07-11 09:00:00'),
(1, '2024-07-10 09:00:00');
-- Previous longest streak
INSERT INTO habit_tracker (user_habit_id, completed_at) VALUES 
(1, '2024-07-06 09:00:00'),
(1, '2024-07-05 09:00:00'),
(1, '2024-07-04 09:00:00'),
(1, '2024-07-03 09:00:00'),
(1, '2024-07-02 09:00:00'),
(1, '2024-07-01 09:00:00'),
(1, '2024-06-30 09:00:00'),
(1, '2024-06-29 09:00:00');

-- Alice's "Exercise" habit (current streak 3, longest streak 3)
-- Current streak
INSERT INTO habit_tracker (user_habit_id, completed_at) VALUES 
(2, '2024-07-13 18:00:00'),
(2, '2024-07-06 18:00:00'),
(2, '2024-06-29 18:00:00');
-- Previous longest streak
-- (same as current streak for this habit)

-- Bob's "Exercise" habit (current streak 5, longest streak 5)
-- Current streak
INSERT INTO habit_tracker (user_habit_id, completed_at) VALUES 
(3, '2024-07-13 18:00:00'),
(3, '2024-07-06 18:00:00'),
(3, '2024-06-29 18:00:00'),
(3, '2024-06-22 18:00:00'),
(3, '2024-06-15 18:00:00');
-- Previous longest streak
-- (same as current streak for this habit)

-- Bob's "Park Walk" habit (current streak 2, longest streak 3)
-- Current streak
INSERT INTO habit_tracker (user_habit_id, completed_at) VALUES 
(4, '2024-07-13 07:00:00'),
(4, '2024-07-06 07:00:00');
-- Previous longest streak
INSERT INTO habit_tracker (user_habit_id, completed_at) VALUES 
(4, '2024-06-22 07:00:00'),
(4, '2024-06-15 07:00:00'),
(4, '2024-06-08 07:00:00');

-- Bob's "Journal" habit (current streak 0, longest streak 1)
-- Previous longest streak
INSERT INTO habit_tracker (user_habit_id, completed_at) VALUES 
(5, '2024-07-10 20:00:00');
