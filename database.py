"""SQLite storage for FindIt. One 'reports' table holds lost + found reports."""

import os
import sqlite3

# Database file lives next to the code so a fresh clone works with zero setup.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "findit.db")


def get_connection():
    """Open a new SQLite connection (caller closes it)."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # rows behave like dicts
    return conn


def init_db():
    """Create the database file and reports table if they do not exist."""
    conn = get_connection()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL CHECK (type IN ('lost', 'found')),
                item_name TEXT NOT NULL,
                category TEXT NOT NULL,
                color TEXT NOT NULL,
                location TEXT NOT NULL,
                description TEXT DEFAULT '',
                report_date TEXT NOT NULL,
                contact TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def add_report(report_type, item_name, category, color, location,
               description, report_date, contact=""):
    """Insert one report. Returns the new row id. Uses parameterized SQL."""
    conn = get_connection()
    try:
        cur = conn.execute(
            """INSERT INTO reports
               (type, item_name, category, color, location, description, report_date, contact)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (report_type, item_name.strip(), category.strip(), color.strip(),
             location.strip(), description.strip(), str(report_date), contact.strip()),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def get_reports(report_type=None):
    """Fetch all reports, newest first. report_type is 'lost', 'found' or None."""
    conn = get_connection()
    try:
        if report_type in ("lost", "found"):
            rows = conn.execute(
                "SELECT * FROM reports WHERE type = ? ORDER BY report_date DESC, id DESC",
                (report_type,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM reports ORDER BY report_date DESC, id DESC"
            ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_report_by_id(report_id):
    """Fetch a single report by id, or None if it does not exist."""
    conn = get_connection()
    try:
        row = conn.execute("SELECT * FROM reports WHERE id = ?", (report_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def search_reports(keyword="", category="All", location="", report_type="All"):
    """Simple filtered search using LIKE. Empty filters match everything."""
    conn = get_connection()
    try:
        query = "SELECT * FROM reports WHERE 1=1"
        params = []
        if keyword.strip():
            query += " AND item_name LIKE ?"
            params.append("%" + keyword.strip() + "%")
        if category != "All":
            query += " AND category = ?"
            params.append(category)
        if location.strip():
            query += " AND location LIKE ?"
            params.append("%" + location.strip() + "%")
        if report_type in ("lost", "found"):
            query += " AND type = ?"
            params.append(report_type)
        query += " ORDER BY report_date DESC, id DESC"
        rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def count_reports():
    """Return (lost_count, found_count) for the home dashboard."""
    conn = get_connection()
    try:
        lost = conn.execute("SELECT COUNT(*) FROM reports WHERE type = 'lost'").fetchone()[0]
        found = conn.execute("SELECT COUNT(*) FROM reports WHERE type = 'found'").fetchone()[0]
        return lost, found
    finally:
        conn.close()
