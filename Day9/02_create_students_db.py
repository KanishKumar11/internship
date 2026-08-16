"""
02_create_students_db.py - Build students.db (run this BEFORE Day 9 starts)

TEACHES : CREATE TABLE + INSERT + commit, and the idea that a database is
          the same table you already know from students.csv - only now the
          column types and rules are enforced by software.
SLIDE   : Day 9, Slide 6 - What Is a Database? (deck page 06/25)
RUN     : python 02_create_students_db.py

EXPECTED OUTPUT IN THE TERMINAL
        Created students.db with 8 students
        (1, 'Aarav', 20, 'Amritsar', 'BCA', 85)
        ...
        (8, 'Karan', 22, 'Ludhiana', 'BCA', 82)

SETUP ORDER
    Run this first. Files 03, 04 and 05 all read students.db and will fail
    with "no such table: students" if it does not exist yet.
    Safe to re-run: it rebuilds the table from scratch every time, so the
    ids are always 1-8 and the demo output never drifts.
"""

import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).with_name("students.db")

# The first 8 rows of students.csv, as tuples in column order. id is NOT
# in here - AUTOINCREMENT makes SQLite assign 1, 2, 3... itself.
STUDENTS: list[tuple[str, int, str, str, int]] = [
    ("Aarav", 20, "Amritsar", "BCA", 85),
    ("Priya", 21, "Jalandhar", "BCA", 92),
    ("Rahul", 22, "Amritsar", "BSc-IT", 78),
    ("Meera", 20, "Ludhiana", "BCA", 88),
    ("Sanjana", 21, "Amritsar", "BCA", 91),
    ("Vikram", 23, "Jalandhar", "BSc-IT", 75),
    ("Anjali", 20, "Amritsar", "BCA", 89),
    ("Karan", 22, "Ludhiana", "BCA", 82),
]


def create_students_db() -> int:
    """Rebuild students.db from scratch. Return how many rows were inserted."""
    # connect() opens the file - and CREATES it if it does not exist. That
    # is why there is no "make an empty database" step anywhere.
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Dropping first makes this script safe to run twice. Without it, a
    # second run would append another 8 students and every id on the slides
    # would be wrong.
    cursor.execute("DROP TABLE IF EXISTS students")

    cursor.execute(
        """
        CREATE TABLE students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            city TEXT,
            branch TEXT,
            marks INTEGER
        )
        """
    )

    # executemany runs the same INSERT once per tuple. The ? placeholders
    # are filled in by SQLite - never build this string with an f-string.
    cursor.executemany(
        "INSERT INTO students (name, age, city, branch, marks) VALUES (?, ?, ?, ?, ?)",
        STUDENTS,
    )

    # Nothing is written to the file until commit(). Forget this line and
    # the database is empty the next time you open it - the single most
    # common "my data disappeared" bug.
    conn.commit()
    conn.close()
    return len(STUDENTS)


def print_all_students() -> None:
    """Read the table back so we can see the ids SQLite assigned."""
    conn = sqlite3.connect(DB_FILE)
    for row in conn.execute("SELECT * FROM students"):
        print(row)
    conn.close()


inserted = create_students_db()
print(f"Created {DB_FILE.name} with {inserted} students")
print_all_students()
