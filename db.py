import sqlite3
from pathlib import Path

DB_NAME = "support.db"

def _connect():
    return sqlite3.connect(DB_NAME)

def init_db():
    Path(DB_NAME).touch(exist_ok=True)
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            message TEXT,
            department TEXT CHECK(department IN ('technical','sales')),
            status TEXT DEFAULT 'open' CHECK(status IN ('open','in_progress','closed')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    conn.commit()
    conn.close()

def add_request(user_id: int, username: str, message: str, department: str):
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO requests (user_id, username, message, department) VALUES (?, ?, ?, ?)",
        (user_id, username, message, department),
    )
    conn.commit()
    conn.close()

def get_requests(status: str = "open", department: str | None = None):
    conn = _connect()
    cur = conn.cursor()
    if department:
        cur.execute(
            "SELECT * FROM requests WHERE status=? AND department=? ORDER BY created_at DESC",
            (status, department),
        )
    else:
        cur.execute(
            "SELECT * FROM requests WHERE status=? ORDER BY created_at DESC",
            (status,),
        )
    rows = cur.fetchall()
    conn.close()
    return rows

def update_status(request_id: int, status: str):
    conn = _connect()
    cur = conn.cursor()
    cur.execute("UPDATE requests SET status=? WHERE id=?", (status, request_id))
    conn.commit()
    conn.close()

def get_request(request_id: int):
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM requests WHERE id=?", (request_id,))
    row = cur.fetchone()
    conn.close()
    return row
