CREATE TABLE IF NOT EXISTS growth_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    raw_text TEXT,
    summary TEXT
);
