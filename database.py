
import sqlite3

def get_connection():
    conn = sqlite3.connect("scamshield.db")
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            severity TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_alert(title, category, description, severity, date):
    conn = get_connection()

    cursor = conn.execute("""
        INSERT INTO alerts (title, category, description, severity, date)
        VALUES (?, ?, ?, ?, ?)
    """, (title, category, description, severity, date))

    alert_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return alert_id


def read_alerts():
    conn = get_connection()

    rows = conn.execute(
        "SELECT * FROM alerts ORDER BY id DESC"
    ).fetchall()

    alerts = [dict(row) for row in rows]

    conn.close()

    return alerts
