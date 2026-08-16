"""
16_crud_demo.py - CRUD: Create, Read, Update, Delete

TEACHES : The four operations that are the entire database API, each in
          its own helper function - the open -> work -> close shape you
          will paste straight into a Streamlit app in file 21.
SLIDE   : Day 10, Slide 6 - SQLite CRUD Operations (deck page 06/18)
RUN     : python 16_crud_demo.py

EXPECTED OUTPUT IN THE TERMINAL
        START - 3 expenses, total 1,250.00
        CREATE - inserted id 4: 250.00 Entertainment
          -> 4 expenses, total 1,500.00
        READ   - SELECT * ORDER BY id
          ... 4 rows printed
        READ   - WHERE category = 'Food' -> 1 row
        UPDATE - id 4: 250.00 -> 275.50  (1 row changed)
          -> total 1,525.50
        DELETE - id 4  (1 row changed)
          -> back to 3 expenses, total 1,250.00
    It ends where it started, so the file is safe to run repeatedly.

REQUIRES
    expenses.db - run 15_sqlite_full_pattern.py first.
"""

import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).with_name("expenses.db")


def create_expense(amount: float, category: str, date: str, note: str) -> int:
    """CREATE - insert one expense. Returns the id SQLite assigned."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)",
        (amount, category, date, note),
    )
    conn.commit()
    # lastrowid is the id AUTOINCREMENT just handed out. You need it
    # whenever the caller has to refer to the row it created - an edit
    # link, a delete button, a foreign key in a child table.
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def read_expenses() -> list[tuple]:
    """READ - every expense, oldest first."""
    conn = sqlite3.connect(DB_FILE)
    rows = conn.execute("SELECT * FROM expenses ORDER BY id").fetchall()
    conn.close()
    return rows


def read_by_category(category: str) -> list[tuple]:
    """READ - only the expenses in one category."""
    conn = sqlite3.connect(DB_FILE)
    # The category is a value, so it is a ? - even though it comes from our
    # own code today, it will come from a selectbox tomorrow.
    rows = conn.execute("SELECT * FROM expenses WHERE category = ?", (category,)).fetchall()
    conn.close()
    return rows


def update_amount(expense_id: int, new_amount: float) -> int:
    """UPDATE - change one expense's amount. Returns rows changed."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # THE DANGEROUS ONE. UPDATE without a WHERE clause rewrites EVERY row
    # in the table, and there is no undo. Write the WHERE first, then the
    # SET - it is a habit worth building now.
    cursor.execute(
        "UPDATE expenses SET amount = ? WHERE id = ?",
        (new_amount, expense_id),
    )
    conn.commit()
    # rowcount says how many rows the statement actually touched. 0 means
    # the WHERE matched nothing - useful, because SQLite does not treat
    # "updated nothing" as an error.
    changed = cursor.rowcount
    conn.close()
    return changed


def delete_expense(expense_id: int) -> int:
    """DELETE - remove one expense by id. Returns rows changed."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Same warning as UPDATE: DELETE FROM expenses with no WHERE empties
    # the whole table. Always delete by primary key.
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    changed = cursor.rowcount
    conn.close()
    return changed


def summary() -> str:
    """A one-line count + total, for printing between the steps."""
    conn = sqlite3.connect(DB_FILE)
    count = conn.execute("SELECT COUNT(*) FROM expenses").fetchone()[0]
    total = conn.execute("SELECT SUM(amount) FROM expenses").fetchone()[0] or 0.0
    conn.close()
    return f"{count} expenses, total {total:,.2f}"


print(f"START  - {summary()}")

# --- C: CREATE ----------------------------------------------------------
new_id = create_expense(250.00, "Entertainment", "2026-08-03", "Movie ticket")
print(f"\nCREATE - inserted id {new_id}: 250.00 Entertainment")
print(f"  -> {summary()}")

# --- R: READ ------------------------------------------------------------
print("\nREAD   - SELECT * ORDER BY id")
for row in read_expenses():
    print(f"  {row}")

food = read_by_category("Food")
print(f"\nREAD   - WHERE category = 'Food' -> {len(food)} row(s)")
for row in food:
    print(f"  {row}")

# --- U: UPDATE ----------------------------------------------------------
changed = update_amount(new_id, 275.50)
print(f"\nUPDATE - id {new_id}: 250.00 -> 275.50  ({changed} row changed)")
print(f"  -> {summary()}")

# --- D: DELETE ----------------------------------------------------------
changed = delete_expense(new_id)
print(f"\nDELETE - id {new_id}  ({changed} row changed)")
print(f"  -> {summary()}")

# Deleting the same id again matches nothing. Not an error - just 0 rows.
print(f"  deleting id {new_id} again changes {delete_expense(new_id)} rows (it is already gone)")

# NOTE ON THE IDS: AUTOINCREMENT never reuses a number. Run this file again
# and the new expense gets id 5, then 6 - the deleted 4 is not recycled.
