import sqlite3
import os
from pathlib import Path
from datetime import datetime

if "DB_PATH" not in os.environ:
    os.environ["DB_PATH"] = str(Path(__file__).parent.parent / "data" / "kohvilogi.db")
DB_PATH = Path(os.environ["DB_PATH"])
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            coffee_type TEXT DEFAULT '',
            amount REAL NOT NULL,
            currency TEXT DEFAULT 'EUR',
            date TEXT NOT NULL,
            notes TEXT DEFAULT '',
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def add_expense(item: str, amount: float, currency: str = "EUR", coffee_type: str = "", date: str | None = None, notes: str = "") -> int:
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO expenses (item, coffee_type, amount, currency, date, notes, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (item, coffee_type, amount, currency, date, notes, datetime.now().isoformat()),
    )
    conn.commit()
    rowid = cur.lastrowid or 0
    conn.close()
    return rowid


def get_expenses(date: str = None, limit: int = 100) -> list:
    conn = get_db()
    if date:
        rows = conn.execute(
            "SELECT * FROM expenses WHERE date = ? ORDER BY created_at DESC LIMIT ?",
            (date, limit),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM expenses ORDER BY created_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_today_total() -> dict:
    today = datetime.now().strftime("%Y-%m-%d")
    conn = get_db()
    rows = conn.execute(
        "SELECT currency, COALESCE(SUM(amount), 0) as total FROM expenses WHERE date = ? GROUP BY currency ORDER BY currency",
        (today,),
    ).fetchall()
    conn.close()
    return {r["currency"]: r["total"] for r in rows}


def get_daily_summary(days: int = 7) -> list:
    conn = get_db()
    rows = conn.execute(
        "SELECT date, currency, SUM(amount) as total, COUNT(*) as count FROM expenses GROUP BY date, currency ORDER BY date DESC LIMIT ?",
        (days * 3,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_expense(expense_id: int) -> bool:
    conn = get_db()
    cur = conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    deleted = cur.rowcount > 0
    conn.close()
    return deleted


def get_monthly_stats(year_month: str) -> dict:
    """Return monthly stats: total by currency, favorite coffee, daily breakdown."""
    conn = get_db()
    # Total by currency
    currency_rows = conn.execute(
        "SELECT currency, COALESCE(SUM(amount), 0) as total, COUNT(*) as count FROM expenses WHERE strftime('%Y-%m', date) = ? GROUP BY currency",
        (year_month,),
    ).fetchall()

    # Favorite coffee type
    fav_rows = conn.execute(
        "SELECT coffee_type, COUNT(*) as cnt FROM expenses WHERE strftime('%Y-%m', date) = ? AND coffee_type != '' GROUP BY coffee_type ORDER BY cnt DESC LIMIT 3",
        (year_month,),
    ).fetchall()

    # Daily breakdown
    daily_rows = conn.execute(
        "SELECT date, COUNT(*) as count, SUM(amount) as total FROM expenses WHERE strftime('%Y-%m', date) = ? AND currency = 'EUR' GROUP BY date ORDER BY date",
        (year_month,),
    ).fetchall()

    # Coffee type breakdown
    type_rows = conn.execute(
        "SELECT coffee_type, COUNT(*) as count, SUM(amount) as total FROM expenses WHERE strftime('%Y-%m', date) = ? AND currency = 'EUR' AND coffee_type != '' GROUP BY coffee_type ORDER BY count DESC",
        (year_month,),
    ).fetchall()

    conn.close()
    return {
        "by_currency": {r["currency"]: {"total": r["total"], "count": r["count"]} for r in currency_rows},
        "favorites": [{"type": r["coffee_type"], "count": r["cnt"]} for r in fav_rows],
        "daily": [dict(r) for r in daily_rows],
        "by_type": [{"type": r["coffee_type"], "count": r["count"], "total": r["total"]} for r in type_rows],
    }
