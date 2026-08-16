"""
04_cursor_explained.py - What a cursor actually is

TEACHES : Connection vs cursor, that ONE cursor can run many queries in
          sequence, and the difference between fetchall() (a list of
          tuples) and fetchone() (a single tuple, or None).
SLIDE   : Day 9, Slide 16 - The Cursor (deck page 16/25)
RUN     : python 04_cursor_explained.py

EXPECTED OUTPUT IN THE TERMINAL
        Query 1 - SELECT * (fetchall)
          8 rows returned, first row: (1, 'Aarav', 20, 'Amritsar', 'BCA', 85)
        Query 2 - COUNT(*) (fetchone)
          (8,)  -> 8 students
        Query 3 - DISTINCT city (fetchall)
          ('Amritsar',) ('Jalandhar',) ('Ludhiana',)
        After close(): using the cursor raises ProgrammingError

REQUIRES
    students.db - run 02_create_students_db.py first.
"""

import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).with_name("students.db")

# THE MENTAL MODEL
#   The connection is the pipe to the database file.
#   The cursor is your remote control - you press buttons (execute) on it.
#   fetchall() / fetchone() are what pull the results back down the pipe.
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# --- Query 1: fetchall returns a LIST of tuples -------------------------
cursor.execute("SELECT * FROM students")
all_students = cursor.fetchall()
print("Query 1 - SELECT * (fetchall)")
print(f"  {len(all_students)} rows returned, first row: {all_students[0]}")

# --- Query 2: the SAME cursor, reused -----------------------------------
# You do not need a new cursor per query. Running execute() again simply
# throws away the previous result set and holds the new one.
cursor.execute("SELECT COUNT(*) FROM students")

# fetchone() returns ONE tuple instead of a list of them. An aggregate like
# COUNT always returns exactly one row, so fetchone is the natural fit -
# and the [0] is how you get the number out of the tuple.
count_row = cursor.fetchone()
print("Query 2 - COUNT(*) (fetchone)")
print(f"  {count_row}  -> {count_row[0]} students")

# --- Query 3: same cursor again -----------------------------------------
cursor.execute("SELECT DISTINCT city FROM students")
cities = cursor.fetchall()
print("Query 3 - DISTINCT city (fetchall)")
# Each row is still a tuple, even with only one column - hence ('Amritsar',)
# with that trailing comma. row[0] is the plain string.
print("  " + " ".join(str(row) for row in cities))
print("  as plain strings: " + ", ".join(row[0] for row in cities))

# --- Closing kills the cursor too ---------------------------------------
conn.close()
try:
    cursor.execute("SELECT * FROM students")
except sqlite3.ProgrammingError as error:
    # Proof of the slide's analogy: hang up the phone and the person you
    # were speaking through cannot say anything else.
    print(f"After close(): using the cursor raises ProgrammingError - {error}")
