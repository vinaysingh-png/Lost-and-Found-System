"""
database.py
-----------
This file handles everything related to the database.

We are using SQLite because it does not need a separate server -
it just stores everything in a single file called lostfound.db
"""

import sqlite3

DB_NAME = "lostfound.db"


def get_connection():
    """
    Opens and returns a connection to the database.
    We set row_factory so that we can access columns by name,
    like item["title"] instead of item[0].
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Creates the 'items' table if it does not already exist.
    This function is safe to run every time the app starts.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_type TEXT NOT NULL,          -- 'lost' or 'found'
            title TEXT NOT NULL,              -- short name of the item
            category TEXT NOT NULL,           -- e.g. Electronics, ID Card, Bottle
            description TEXT,                 -- more details about the item
            location TEXT,                    -- where it was lost/found
            date_reported TEXT NOT NULL,      -- date the report was made
            reporter_name TEXT NOT NULL,      -- name of the person reporting
            reporter_contact TEXT NOT NULL,   -- phone/email to contact them
            image_filename TEXT,              -- filename of uploaded photo (optional)
            status TEXT NOT NULL DEFAULT 'unresolved'  -- 'unresolved' or 'claimed'
        )
    """)

    conn.commit()
    conn.close()


def init_admin_table():
    """
    Creates a simple 'admin' table with one default admin user.
    Username: admin
    Password: admin123
    (For a college project, storing the password in plain text is
    fine and easy to explain. In a real product we would hash it.)
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    # Only add the default admin if the table is empty
    cursor.execute("SELECT COUNT(*) FROM admin")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute(
            "INSERT INTO admin (username, password) VALUES (?, ?)",
            ("admin", "admin123")
        )

    conn.commit()
    conn.close()
