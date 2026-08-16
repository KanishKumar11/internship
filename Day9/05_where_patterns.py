"""
05_where_patterns.py - The WHERE clause, five patterns

TEACHES : WHERE as the SQL equivalent of a pandas boolean mask - single
          condition, AND, OR, LIKE, IN - and the ? placeholder, which is
          the only safe way to put a Python value into a query.
SLIDE   : Day 9, Slide 17 - The WHERE Clause (deck page 17/25)
RUN     : python 05_where_patterns.py

EXPECTED OUTPUT IN THE TERMINAL
    Five labelled result sets from students.db:
        1. age > 20                      -> 5 students
        2. age > 20 AND Amritsar         -> 2 students (Rahul, Sanjana)
        3. age < 20 OR age > 22          -> 1 student  (Vikram)
        4. name LIKE 'A%'                -> 2 students (Aarav, Anjali)
        5. city IN (Amritsar, Jalandhar) -> 6 students
    Then #6: the same query as #2, written with ? placeholders - same two
    rows, which is the point. The placeholders change the safety, not the
    result.

REQUIRES
    students.db - run 02_create_students_db.py first.
"""

import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).with_name("students.db")


def show(label: str, rows: list[tuple]) -> None:
    """Print a labelled result set, one row per line."""
    print(f"\n{label}  ({len(rows)} rows)")
    for row in rows:
        print(f"  {row}")


conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# --- 1. A single condition ----------------------------------------------
# The pandas equivalent from Day 6: df[df["age"] > 20]
cursor.execute("SELECT * FROM students WHERE age > 20")
show("1. WHERE age > 20", cursor.fetchall())

# --- 2. AND - both conditions must hold ---------------------------------
# Triple quotes let a long query span lines. SQL ignores the line breaks;
# they are purely for the human reading it.
cursor.execute(
    """
    SELECT * FROM students
    WHERE age > 20 AND city = 'Amritsar'
    """
)
show("2. WHERE age > 20 AND city = 'Amritsar'", cursor.fetchall())

# --- 3. OR - either condition is enough ---------------------------------
cursor.execute("SELECT * FROM students WHERE age < 20 OR age > 22")
show("3. WHERE age < 20 OR age > 22", cursor.fetchall())

# --- 4. LIKE - pattern matching -----------------------------------------
# % means "any characters here". 'A%' = starts with A. '%a' = ends with a.
# '%ee%' = contains "ee". LIKE is case-insensitive for ASCII in SQLite.
cursor.execute("SELECT * FROM students WHERE name LIKE 'A%'")
show("4. WHERE name LIKE 'A%'", cursor.fetchall())

# --- 5. IN - match any value in a list ----------------------------------
# Shorter than city = 'Amritsar' OR city = 'Jalandhar'.
cursor.execute("SELECT * FROM students WHERE city IN ('Amritsar', 'Jalandhar')")
show("5. WHERE city IN ('Amritsar', 'Jalandhar')", cursor.fetchall())

# --- The same query, with ? placeholders --------------------------------
# THE RULE: any value that comes from a variable - a form field, a
# dropdown, a function argument - goes in as ?, with the values in a tuple
# as the second argument to execute().
#
# NEVER build SQL with an f-string:
#     f"SELECT * FROM students WHERE city = '{city}'"      # UNSAFE
# If city ever holds  '; DROP TABLE students; --  that f-string hands the
# database a delete command. With ?, SQLite treats the value as data, and
# a student named "'; DROP TABLE students; --" is just a name that matches
# nothing. This is SQL injection, and ? is the entire fix.
minimum_age = 20
selected_city = "Amritsar"
cursor.execute(
    "SELECT * FROM students WHERE age > ? AND city = ?",
    (minimum_age, selected_city),  # a tuple, in the order the ?s appear
)
show(f"6. Parameterised: age > ? AND city = ?  ({minimum_age}, {selected_city})", cursor.fetchall())

conn.close()
