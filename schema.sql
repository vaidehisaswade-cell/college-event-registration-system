-- College Event Registration System schema
PRAGMA foreign_keys = ON;

CREATE TABLE events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT NOT NULL,
    category TEXT NOT NULL,
    event_date TEXT NOT NULL,
    venue TEXT NOT NULL,
    capacity INTEGER NOT NULL CHECK (capacity > 0),
    description TEXT DEFAULT ''
);

CREATE TABLE students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    department TEXT NOT NULL,
    year_of_study INTEGER NOT NULL CHECK (year_of_study BETWEEN 1 AND 4)
);

CREATE TABLE registrations (
    registration_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    registration_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Registered'
        CHECK (status IN ('Registered', 'Cancelled', 'Attended')),
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE,
    UNIQUE (student_id, event_id)
);

-- Example JOIN query used for a registration report:
SELECT r.registration_id, s.full_name, s.email, e.event_name,
       r.registration_date, r.status
FROM registrations AS r
JOIN students AS s ON r.student_id = s.student_id
JOIN events AS e ON r.event_id = e.event_id;
