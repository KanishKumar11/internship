"""
14_alter_drop_demo.py - ALTER TABLE and DROP TABLE

TEACHES : Changing a table after it already holds data - ADD COLUMN (and
          what happens to the rows already there), RENAME COLUMN, RENAME
          TO - and DROP TABLE IF EXISTS, the safe way to delete one.
SLIDE   : Day 10, Slide 4 - DDL Deep-Dive, ALTER + DROP (deck page 04/18)
RUN     : python 14_alter_drop_demo.py

EXPECTED OUTPUT IN THE TERMINAL
    Five labelled steps, each printing the table before and after:
        1. CREATE  -> columns: id, amount, note  | 2 rows
        2. ADD COLUMN payment_method TEXT DEFAULT 'Cash'
                   -> the existing rows all read 'Cash' - the default was
                      applied backwards over data that already existed
        3. RENAME COLUMN note TO description  -> data untouched
        4. RENAME TO expense_entries          -> same table, new name
        5. DROP TABLE IF EXISTS expense_entries -> gone; running DROP
                                                  twice does not raise

BUILDS
    playground.db - a scratch file used only by this demo. Slide 4 runs
    these statements against the real expenses table; doing that live
    would rename a column the rest of today's files still read, so the
    same statements are run here on a throwaway table instead. Nothing in
    this file can damage expenses.db. Safe to re-run.
"""

import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).with_name("playground.db")


def column_names(conn: sqlite3.Connection, table: str) -> list[str]:
    """Return a table's column names, in order, straight from SQLite."""
    # PRAGMA table_info returns one row per column; index 1 is the name.
    # A table name cannot be a ? placeholder - placeholders stand for
    # values, never identifiers - so this is formatted in. Safe here
    # because `table` is a hard-coded string in this file, never input.
    return [row[1] for row in conn.execute(f"PRAGMA table_info({table})")]


def show(conn: sqlite3.Connection, table: str, label: str) -> None:
    """Print a table's columns and every row in it."""
    print(f"\n{label}")
    print(f"  columns: {', '.join(column_names(conn, table))}")
    for row in conn.execute(f"SELECT * FROM {table}"):
        print(f"  {row}")


conn = sqlite3.connect(DB_FILE)

# --- 1. Start from a clean table ---------------------------------------
conn.execute("DROP TABLE IF EXISTS test_table")
conn.execute("DROP TABLE IF EXISTS expense_entries")
conn.execute(
    """
    CREATE TABLE test_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        note TEXT
    )
    """
)
conn.executemany(
    "INSERT INTO test_table (amount, note) VALUES (?, ?)",
    [(450.0, "Lunch with team"), (120.0, "Auto to college")],
)
conn.commit()
show(conn, "test_table", "1. CREATE TABLE test_table")

# --- 2. ADD COLUMN ------------------------------------------------------
# The rows already in the table cannot be left without a value for the new
# column, so SQLite backfills them - with the DEFAULT if you gave one, and
# with NULL if you did not. This is the whole reason to specify a DEFAULT.
conn.execute("ALTER TABLE test_table ADD COLUMN payment_method TEXT DEFAULT 'Cash'")
conn.commit()
show(conn, "test_table", "2. ALTER TABLE ... ADD COLUMN payment_method TEXT DEFAULT 'Cash'")
print("  -> both existing rows were backfilled with the default")

# --- 3. RENAME COLUMN ---------------------------------------------------
# Renames the column and leaves the data exactly where it is. Any SQL you
# have written elsewhere that says "name" now breaks, which is why this is
# a bigger decision than it looks.
conn.execute("ALTER TABLE test_table RENAME COLUMN note TO description")
conn.commit()
show(conn, "test_table", "3. ALTER TABLE ... RENAME COLUMN note TO description")

# --- 4. RENAME the whole table -----------------------------------------
conn.execute("ALTER TABLE test_table RENAME TO expense_entries")
conn.commit()
show(conn, "expense_entries", "4. ALTER TABLE test_table RENAME TO expense_entries")

# --- 5. DROP TABLE ------------------------------------------------------
# DROP deletes the table AND every row in it, with no undo and no
# confirmation. IF NOT EXISTS protects a CREATE; IF EXISTS protects a DROP.
conn.execute("DROP TABLE IF EXISTS expense_entries")
conn.commit()
print("\n5. DROP TABLE IF EXISTS expense_entries")

remaining = conn.execute(
    "SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?",
    ("expense_entries",),
).fetchall()
print(f"  tables named 'expense_entries' still in the database: {len(remaining)}")

# Running it a second time is a no-op rather than an error - that is what
# IF EXISTS buys you. Without it, this raises "no such table".
conn.execute("DROP TABLE IF EXISTS expense_entries")
print("  ran DROP a second time - IF EXISTS made it a no-op, not an error")

# WHAT SQLITE CANNOT DO
#   Other databases support ALTER TABLE ... DROP COLUMN and changing a
#   column's type. Older SQLite versions support neither. The workaround is
#   always the same: CREATE a new table with the shape you want, INSERT
#   INTO new SELECT ... FROM old, DROP the old, RENAME the new.
conn.close()
