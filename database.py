import sqlite3

DB_PATH = "urls.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS urls (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code  TEXT UNIQUE NOT NULL,
            long_url    TEXT NOT NULL,
            created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_short_code ON urls (short_code)"
    )
    conn.commit()
    conn.close()


def insert_url(short_code, long_url):
    conn = get_connection()
    conn.execute(
        "INSERT INTO urls (short_code, long_url) VALUES (?, ?)",
        (short_code, long_url),
    )
    conn.commit()
    conn.close()


def get_url(short_code):
    conn = get_connection()
    row = conn.execute(
        "SELECT long_url FROM urls WHERE short_code = ?", (short_code,)
    ).fetchone()
    conn.close()
    return row["long_url"] if row else None