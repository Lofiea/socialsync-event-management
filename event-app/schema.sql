CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    start_date TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_date TEXT NOT NULL,
    end_time TEXT NOT NULL,
    location TEXT NOT NULL,
    is_offline BOOLEAN NOT NULL,
    capacity INTEGER,
    visibility TEXT NOT NULL,
    host TEXT NOT NULL,
    age_tag TEXT,
    event_type TEXT NOT NULL,
    budget TEXT,
    notes TEXT
);
