import sqlite3
from datetime import date, datetime, timedelta
from config import DB_PATH


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        with open("storage/schema.sql", "r") as f:
            conn.executescript(f.read())


def save_log(raw_text, summary, tags=None, mood=None):
    with sqlite3.connect(DB_PATH) as conn:
        today = date.today().isoformat()
        conn.execute(
            "INSERT INTO growth_logs (date, raw_text, summary, tags, mood) VALUES (?, ?, ?, ?, ?)",
            (today, raw_text, summary, ",".join(tags or []), ",".join(mood or []))
        )
        conn.commit()


def get_recent_logs(days=7):
    since = (datetime.now() - timedelta(days=days)).date().isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "SELECT * FROM growth_logs WHERE date >= ? ORDER BY date DESC", (since,)
        )
        return cursor.fetchall()
