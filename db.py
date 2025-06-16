import sqlite3

def connect_db():
    return sqlite3.connect("data.db")

def init_db():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                type TEXT CHECK(type IN ('Spend', 'Borrow', 'Lend')),
                category TEXT,
                amount REAL,
                person TEXT,
                notes TEXT
            )
        """)
        conn.commit()
