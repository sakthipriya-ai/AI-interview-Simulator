import sqlite3

def create_database():

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    # USERS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        email TEXT,
        password TEXT
    )
    """)

    # INTERVIEW HISTORY TABLE (IMPORTANT FIX)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS interview_history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        score INTEGER
    )
    """)

    conn.commit()
    conn.close()