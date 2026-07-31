import sqlite3
import os

DB_PATH = os.environ.get("DB_PATH", "tasks.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    priority TEXT DEFAULT 'medium',
    completed INTEGER DEFAULT 0
);
"""


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()


def execute(query, params=()):
    conn = get_connection()
    cursor = conn.execute(query, params)
    conn.commit()
    rows = cursor.fetchall()
    lastrowid = cursor.lastrowid
    conn.close()
    return rows, lastrowid


def fetch_one(query, params=()):
    conn = get_connection()
    row = conn.execute(query, params).fetchone()
    conn.close()
    return row


def fetch_all(query, params=()):
    conn = get_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return rows


init_db()
