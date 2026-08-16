"""
17_with_context_manager.py - The with block, and what it really does

TEACHES : Manual open/work/close and its failure mode, then what
          `with sqlite3.connect(...)` actually gives you - an automatic
          commit on success and an automatic ROLLBACK on error - and the
          one thing it does NOT do, which is close the connection.
SLIDE   : Day 10, Slide 9 - Pattern, The with Block (deck page 09/18)
RUN     : python 17_with_context_manager.py

EXPECTED OUTPUT IN THE TERMINAL
        1. MANUAL - open, work, close
           3 rows read, connection closed: True
        2. MANUAL + a crash
           ValueError raised. Connection closed? False  <- leaked
        3. with block - the happy path
           inserted 'Coffee' inside the block; after the block: 4 rows
        4. with block - when the body raises
           ValueError raised. Rows now: 4  <- the insert was ROLLED BACK
        5. The catch: is the connection closed after the with block?
           conn.execute() still works -> the connection is STILL OPEN
        6. The fix: with closing(sqlite3.connect(...)) as conn
           committed AND closed: True
        FINAL - back to 3 rows

    Note step 5. Slide 9 says the with block auto-closes. It does not -
    it manages the TRANSACTION, not the connection. Steps 5 and 6 show
    the difference and the fix.

REQUIRES
    expenses.db - run 15_sqlite_full_pattern.py first.
"""

import sqlite3
from contextlib import closing
from pathlib import Path

DB_FILE = Path(__file__).with_name("expenses.db")


def count_rows() -> int:
    """How many expenses are in the table right now?"""
    conn = sqlite3.connect(DB_FILE)
    count = conn.execute("SELECT COUNT(*) FROM expenses").fetchone()[0]
    conn.close()
    return count


def is_closed(conn: sqlite3.Connection) -> bool:
    """True if the connection is closed. There is no .closed attribute, so ask."""
    try:
        conn.execute("SELECT 1")
        return False
    except sqlite3.ProgrammingError:
        return True


# --- 1. The manual pattern ----------------------------------------------
print("1. MANUAL - open, work, close")
conn = sqlite3.connect(DB_FILE)
rows = conn.execute("SELECT * FROM expenses").fetchall()
conn.close()
print(f"   {len(rows)} rows read, connection closed: {is_closed(conn)}")

# --- 2. The manual pattern when something goes wrong --------------------
# This is the real argument against it. The close() line is written, but
# execution never reaches it, so the connection is left open.
print("\n2. MANUAL + a crash")
leaked = sqlite3.connect(DB_FILE)
try:
    leaked.execute("SELECT * FROM expenses")
    raise ValueError("something blew up mid-function")
    leaked.close()  # never runs - unreachable after the raise
except ValueError as error:
    print(f"   ValueError raised. Connection closed? {is_closed(leaked)}  <- leaked")
leaked.close()  # cleaning up after our own demo

# --- 3. The with block, happy path --------------------------------------
# On a clean exit the context manager calls commit() for you. Note there is
# no conn.commit() line anywhere in this block.
print("\n3. with block - the happy path")
with sqlite3.connect(DB_FILE) as conn:
    conn.execute(
        "INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)",
        (60.00, "Food", "2026-08-04", "Coffee"),
    )
print(f"   inserted 'Coffee' inside the block; after the block: {count_rows()} rows")

# --- 4. The with block when the body raises -----------------------------
# THIS is what the with block is actually for. The exception makes it call
# rollback() instead of commit(), so the INSERT above it is undone. The
# table is never left half-written.
print("\n4. with block - when the body raises")
try:
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)",
            (999.00, "Food", "2026-08-04", "This should never be saved"),
        )
        raise ValueError("crash after the insert, before the commit")
except ValueError:
    print(f"   ValueError raised. Rows now: {count_rows()}  <- the insert was ROLLED BACK")

# --- 5. The part the slide gets wrong -----------------------------------
# sqlite3's context manager wraps the TRANSACTION, not the connection. On
# exit it commits or rolls back - and then leaves the connection open.
print("\n5. The catch: is the connection closed after the with block?")
with sqlite3.connect(DB_FILE) as conn:
    conn.execute("SELECT 1")
if is_closed(conn):
    print("   the connection is closed")
else:
    print("   conn.execute() still works -> the connection is STILL OPEN")
    conn.close()

# --- 6. The fix: closing() ----------------------------------------------
# contextlib.closing calls .close() on whatever it wraps when the block
# ends. Nest the two and you get both guarantees: commit-or-rollback from
# sqlite3's manager, and a guaranteed close from closing().
print("\n6. The fix: with closing(sqlite3.connect(...)) as conn")
with closing(sqlite3.connect(DB_FILE)) as conn:
    with conn:  # transaction: commit on success, rollback on error
        conn.execute("DELETE FROM expenses WHERE note = ?", ("Coffee",))
print(f"   committed AND closed: {is_closed(conn)}")

print(f"\nFINAL - back to {count_rows()} rows")

# WHICH ONE SHOULD YOU WRITE?
#   For the small helper functions in tomorrow's app, the plain
#   open -> work -> close pattern is fine and is what the slides show;
#   the functions are three lines long and cannot leak much.
#   For anything that can raise between the open and the close, reach for
#   `with closing(...)`. And remember: a plain `with sqlite3.connect(...)`
#   is about the transaction, not the file handle.
