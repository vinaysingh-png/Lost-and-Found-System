

import os
import sqlite3

# Absolute path, so it works on PythonAnywhere too
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "lostfound.db")


def get_connection():
    
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    
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
    Password: LostFound@2026
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

    
    cursor.execute("SELECT COUNT(*) FROM admin")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute(
            "INSERT INTO admin (username, password) VALUES (?, ?)",
            ("admin", "LostFound@2026")
        )

    conn.commit()
    conn.close()
