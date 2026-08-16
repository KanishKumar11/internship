"""
06_create_table_demo.py - CREATE TABLE with constraints (builds expenses.db)

TEACHES : Every part of a CREATE TABLE statement - IF NOT EXISTS, PRIMARY
          KEY AUTOINCREMENT, NOT NULL, DEFAULT - and what the database
          does when you leave an optional column out of an INSERT.
SLIDE   : Day 9, Slide 18 - DDL Deep-Dive, CREATE TABLE (deck page 18/25)
RUN     : python 06_create_table_demo.py

EXPECTED OUTPUT IN THE TERMINAL
    The column list read back out of the database with PRAGMA table_info:
        cid  name        type     notnull  default            pk
        0    id          INTEGER  0        -                  1
        1    amount      REAL     1        -                  0
        2    category    TEXT     1        'Other'            0
        3    date        TEXT     1        -                  0
        4    note        TEXT     0        -                  0
        5    created_at  TEXT     0        datetime('now')    0
    Then the 20 seeded rows. Look at the last three:
        - id 18 is a complete row
        - id 19 was inserted with no note      -> note is None (NULL)
        - id 20 was inserted with no category  -> category is 'Other'
    ...and every row has a created_at timestamp nobody passed in.
    It ends with "20 rows, total 12,450.00".

SETUP ORDER
    Run this before Day 9's second half. It builds the expenses.db that
    files 09, 10, 11 and 12 all read - 20 rows, exactly as slide 24 says,
    and the 8 Food rows / 5 categories / 12,450 total that Day 10's recap
    slide quotes back at the room.
    Safe to re-run: it seeds only when the table is empty. To rebuild it
    from scratch, delete expenses.db first.
"""

import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).with_name("expenses.db")

# 17 ordinary rows. Column order: amount, category, date, note.
# A None in the note column becomes SQL NULL - that is how "the user left
# the note blank" is stored, and what file 10's IS NULL query finds.
BASE_EXPENSES: list[tuple[float, str, str, str | None]] = [
    (450.00, "Food", "2026-07-28", "Lunch with team"),
    (120.00, "Transport", "2026-07-28", "Auto to college"),
    (680.00, "Books", "2026-07-29", "Python textbook"),
    (4500.00, "Rent", "2026-07-29", None),
    (240.00, "Food", "2026-07-30", "Canteen snacks"),
    (210.00, "Food", "2026-07-30", "Groceries run"),
    (90.00, "Transport", "2026-07-31", "Bus pass top-up"),
    (320.00, "Food", "2026-07-31", "Dinner outside"),
    (180.00, "Transport", "2026-08-01", None),
    (540.00, "Books", "2026-08-01", "Notebooks and pens"),
    (150.00, "Food", "2026-08-02", "Tea and samosa"),
    (300.00, "Other", "2026-08-02", "Phone recharge"),
    (780.00, "Food", "2026-08-03", "Weekend groceries"),
    (230.00, "Transport", "2026-08-03", "Train ticket home"),
    (180.00, "Transport", "2026-08-04", "Auto to station"),
    (380.00, "Books", "2026-08-04", None),
    (900.00, "Food", "2026-08-05", "Monthly mess top-up"),
]

# THE NUMBERS ARE DELIBERATE. Day 10's recap slide (page 03/18) tells the
# room what yesterday's exercise printed: 20 rows, 8 Food expenses, 5
# categories, a 12,450 total. These 17 rows plus the 3 below produce
# exactly that, so the slide and the database agree in front of the class.


def create_table(conn: sqlite3.Connection) -> None:
    """Create the expenses table if it is not already there."""
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL DEFAULT 'Other',
            date TEXT NOT NULL,
            note TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        )
        """
    )
    # IF NOT EXISTS is what makes this safe to call on every single app
    # start-up. Without it, the second run raises
    # "table expenses already exists" and the app dies before it renders.


def print_structure(conn: sqlite3.Connection) -> None:
    """Print the table's own description of itself."""
    # PRAGMA table_info is SQLite asking SQLite what the columns are. It is
    # the fastest way to check that the table you created is the table you
    # meant to create.
    print(f"{'cid':<4} {'name':<11} {'type':<8} {'notnull':<8} {'default':<18} pk")
    for cid, name, col_type, notnull, default, primary_key in conn.execute(
        "PRAGMA table_info(expenses)"
    ):
        shown_default = default if default is not None else "-"
        print(f"{cid:<4} {name:<11} {col_type:<8} {notnull:<8} {shown_default:<18} {primary_key}")


def seed(conn: sqlite3.Connection) -> None:
    """Insert the 20 demo rows - but only into an empty table."""
    already_there = conn.execute("SELECT COUNT(*) FROM expenses").fetchone()[0]
    if already_there:
        print(f"\nexpenses table already has {already_there} rows - not re-seeding.")
        print("Delete expenses.db and run this file again for a clean 20 rows.")
        return

    # Naming the columns (amount, category, date, note) means we do NOT
    # pass id or created_at - SQLite fills those in itself.
    conn.executemany(
        "INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)",
        BASE_EXPENSES,
    )

    # --- The three rows the slide is really about -----------------------
    # 18: everything supplied.
    conn.execute(
        "INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)",
        (150.00, "Food", "2026-08-06", "Coffee with friends"),
    )
    # 19: no note column at all. note has no NOT NULL and no DEFAULT, so it
    # is stored as NULL and comes back to Python as None.
    conn.execute(
        "INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
        (850.00, "Books", "2026-08-06"),
    )
    # 20: no category column. category is NOT NULL - but it has
    # DEFAULT 'Other', and the default is what satisfies the NOT NULL rule.
    # Drop the DEFAULT from the schema and this exact INSERT would fail.
    conn.execute(
        "INSERT INTO expenses (amount, date, note) VALUES (?, ?, ?)",
        (1200.00, "2026-08-06", "Internet bill"),
    )
    conn.commit()


def print_rows(conn: sqlite3.Connection) -> None:
    """Print every row so the applied defaults are visible."""
    print(f"\n{'id':<4} {'amount':>8}  {'category':<14} {'date':<12} {'note':<22} created_at")
    for row in conn.execute("SELECT * FROM expenses ORDER BY id"):
        expense_id, amount, category, date, note, created_at = row
        # None is Python's version of SQL NULL. Printed raw it says "None",
        # so show it as NULL to keep the database vocabulary consistent.
        shown_note = note if note is not None else "NULL"
        print(f"{expense_id:<4} {amount:>8.2f}  {category:<14} {date:<12} {shown_note:<22} {created_at}")


conn = sqlite3.connect(DB_FILE)
create_table(conn)
print(f"Table structure of expenses in {DB_FILE.name}:\n")
print_structure(conn)
seed(conn)
print_rows(conn)

total = conn.execute("SELECT SUM(amount) FROM expenses").fetchone()[0]
row_count = conn.execute("SELECT COUNT(*) FROM expenses").fetchone()[0]
print(f"\n{row_count} rows, total {total:,.2f}")
conn.close()
