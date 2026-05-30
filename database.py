import sqlite3

conn = sqlite3.connect("fitness.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    age INTEGER,
    height REAL,
    weight REAL,
    bmi REAL,
    category TEXT,
    goal TEXT,
    calories INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS auth_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    email TEXT UNIQUE,
    password TEXT
)
""")

try:
    cursor.execute("ALTER TABLE users ADD COLUMN username TEXT")
except sqlite3.OperationalError:
    pass

conn.commit()
conn.close()

print("Database updated successfully")