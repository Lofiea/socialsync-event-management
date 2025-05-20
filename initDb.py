import sqlite3

conn = sqlite3.connect('events.db')  # Connect to the database
c = conn.cursor()

# Create the events table with the new 'is_favorite' column
c.execute('''
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    purpose TEXT,
    description TEXT,
    location TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    type TEXT NOT NULL,
    price REAL NOT NULL,
    attendees INTEGER,
    age_limit TEXT,
    additional_info TEXT,
    image TEXT,
    is_favorite INTEGER DEFAULT 0
)
''')

conn.commit()  # Save changes to the database
conn.close()  # Close the connection

print("events.db created with 'events' table and 'is_favorite' column.")
