"""
15_sqlite_full_pattern.py - The full SQLite pattern (run BEFORE Day 10)

TEACHES : connect -> CREATE TABLE -> INSERT -> commit -> close, then
          reopen and SELECT to prove the data survived. The proof that a
          database file persists without any of Day 8's CSV plumbing.
SLIDE   : Day 10, Slide 5 - Storage Format 02 of 03, SQLite
          (deck page 05/18)
RUN     : python 15_sqlite_full_pattern.py

EXPECTED OUTPUT IN THE TERMINAL
        Connection 1 - writing
          created table 'expenses'
          inserted 3 rows, committed, closed
        Connection 2 - reading (a brand new connection)
          (1, 450.0, 'Food', '2026-08-01', 'Lunch with team')
          (2, 120.0, 'Transport', '2026-08-01', 'Auto to college')
          (3, 680.0, 'Books', '2026-08-02', 'Python textbook')
          3 rows, total 1,250.00
        expenses.db is 12288 bytes on disk  (size will vary slightly)

SETUP ORDER
    Run this first on Day 10. It builds the fresh expenses.db that files
    16, 17, 18, 19 and the three app files all use.
    Safe to re-run: it rebuilds the table from scratch, so the ids are
    always 1-3 and the demo output never drifts.
"""

import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).with_name("expenses.db")

# (amount, category, date, note)
STARTER_EXPENSES: list[tuple[float, str, str, str]] = [
    (450.00, "Food", "2026-08-01", "Lunch with team"),
    (120.00, "Transport", "2026-08-01", "Auto to college"),
    (680.00, "Books", "2026-08-02", "Python textbook"),
]


def build_database() -> None:
    """Connection 1: create the table, insert the starter rows, close."""
    # STEP 1 - CONNECT. Opens expenses.db, creating the file if it is not
    # there. No server, no username, no password: that is SQLite's whole
    # pitch. The database is a file sitting next to your code.
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Dropped so this file is a reliable reset button during the session.
    # A real app would only ever use CREATE TABLE IF NOT EXISTS.
    cursor.execute("DROP TABLE IF EXISTS expenses")

    # STEP 2 - CREATE TABLE. Defines the shape once.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            note TEXT
        )
        """
    )
    print("Connection 1 - writing")
    print("  created table 'expenses'")

    # STEP 3 - INSERT, with ? placeholders. Four columns named, four ?s,
    # four values per tuple. Those three numbers must always agree.
    cursor.executemany(
        "INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)",
        STARTER_EXPENSES,
    )

    # STEP 4 - COMMIT. Until this line the inserts live in a transaction in
    # memory; the file on disk is unchanged. Close without committing and
    # the rows are gone. This is the #1 cause of "my data disappeared".
    conn.commit()

    # STEP 5 - CLOSE. Releases the file.
    conn.close()
    print(f"  inserted {len(STARTER_EXPENSES)} rows, committed, closed")


def read_database() -> None:
    """Connection 2: a fresh connection proves the rows are really on disk."""
    conn = sqlite3.connect(DB_FILE)
    print("\nConnection 2 - reading (a brand new connection)")

    rows = conn.execute("SELECT * FROM expenses ORDER BY id").fetchall()
    for row in rows:
        print(f"  {row}")

    total = conn.execute("SELECT SUM(amount) FROM expenses").fetchone()[0]
    print(f"  {len(rows)} rows, total {total:,.2f}")
    conn.close()


build_database()
read_database()

# The database is one ordinary file. Copy it, email it, commit it to git -
# it travels with the rows inside.
print(f"\n{DB_FILE.name} is {DB_FILE.stat().st_size} bytes on disk")
