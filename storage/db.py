import sqlite3
from datetime import date

DB_PATH = "data/growth_log.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        with open("storage/schema.sql", "r") as f:
            conn.executescript(f.read())

def save_log(raw_text, summary):
    with sqlite3.connect(DB_PATH) as conn:
        today = date.today().isoformat()
        conn.execute(
            "INSERT INTO growth_logs (date, raw_text, summary) VALUES (?, ?, ?)",
            (today, raw_text, summary)
        )
        conn.commit()
