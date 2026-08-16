"""
07_foreign_key_demo.py - FOREIGN KEY: how tables talk to each other

TEACHES : A parent table (students) and a child table (expenses) linked by
          student_id, why SQLite ignores foreign keys unless you switch
          them on, and what the database does when you try to attach a row
          to a parent that does not exist.
SLIDE   : Day 9, Slide 19 - DDL Deep-Dive, FOREIGN KEY (deck page 19/25)
RUN     : python 07_foreign_key_demo.py

EXPECTED OUTPUT IN THE TERMINAL
        Students: 3   Expenses: 5
        JOIN - each expense next to its student:
          Aarav          450.00  Food
          Aarav          120.00  Transport
          Priya          680.00  Books
          Priya          300.00  Food
          Rahul          220.00  Transport
        Inserting an expense for student_id=999 (nobody):
          BLOCKED - IntegrityError: FOREIGN KEY constraint failed
        Expenses after the rejected insert: 5   (nothing was added)

BUILDS
    app.db - a separate file from students.db and expenses.db, because
    the expenses table here has an extra student_id column. File 08 reads
    this same app.db. Safe to re-run: it rebuilds both tables.
"""

import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).with_name("app.db")

# (name, city)
STUDENTS: list[tuple[str, str]] = [
    ("Aarav", "Amritsar"),
    ("Priya", "Jalandhar"),
    ("Rahul", "Amritsar"),
]

# (amount, category, date, student_id) - student_id is the link back to
# the students table. 1 = Aarav, 2 = Priya, 3 = Rahul.
EXPENSES: list[tuple[float, str, str, int]] = [
    (450.00, "Food", "2026-08-01", 1),
    (120.00, "Transport", "2026-08-01", 1),
    (680.00, "Books", "2026-08-02", 2),
    (300.00, "Food", "2026-08-02", 2),
    (220.00, "Transport", "2026-08-03", 3),
]


def build_tables(conn: sqlite3.Connection) -> None:
    """Create the parent and child tables from scratch."""
    # Drop the child first. The parent cannot be dropped while a child
    # still references it - the same rule the FOREIGN KEY enforces on rows.
    conn.execute("DROP TABLE IF EXISTS expenses")
    conn.execute("DROP TABLE IF EXISTS students")

    # The PARENT table. Its id is what the child will point at.
    conn.execute(
        """
        CREATE TABLE students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            city TEXT
        )
        """
    )

    # The CHILD table. student_id is an ordinary INTEGER column - it is the
    # FOREIGN KEY line at the bottom that gives it meaning: "every value in
    # student_id must match an id that exists in students".
    conn.execute(
        """
        CREATE TABLE expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT,
            date TEXT,
            student_id INTEGER,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
        """
    )

    conn.executemany("INSERT INTO students (name, city) VALUES (?, ?)", STUDENTS)
    conn.executemany(
        "INSERT INTO expenses (amount, category, date, student_id) VALUES (?, ?, ?, ?)",
        EXPENSES,
    )
    conn.commit()


conn = sqlite3.connect(DB_FILE)

# THE GOTCHA NOBODY WARNS YOU ABOUT.
# SQLite parses the FOREIGN KEY line but does NOT enforce it unless you
# turn enforcement on, per connection, every time you connect. Comment the
# next line out and the student_id=999 insert below succeeds silently -
# which is exactly how orphaned rows get into real databases.
conn.execute("PRAGMA foreign_keys = ON")

build_tables(conn)

student_count = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
expense_count = conn.execute("SELECT COUNT(*) FROM expenses").fetchone()[0]
print(f"Students: {student_count}   Expenses: {expense_count}")

# --- Using the link: a JOIN --------------------------------------------
# The foreign key stores the relationship. JOIN is how a query uses it.
# ON students.id = expenses.student_id is the line that says which column
# matches which - full detail on this in file 08.
print("\nJOIN - each expense next to its student:")
join_query = """
    SELECT students.name, expenses.amount, expenses.category
    FROM students
    JOIN expenses ON students.id = expenses.student_id
    ORDER BY students.id, expenses.id
"""
for name, amount, category in conn.execute(join_query):
    print(f"  {name:<12} {amount:>8.2f}  {category}")

# --- The constraint doing its job ---------------------------------------
print("\nInserting an expense for student_id=999 (nobody):")
try:
    conn.execute(
        "INSERT INTO expenses (amount, category, date, student_id) VALUES (?, ?, ?, ?)",
        (999.00, "Food", "2026-08-04", 999),
    )
    conn.commit()
    print("  Inserted - foreign keys are NOT being enforced on this connection.")
except sqlite3.IntegrityError as error:
    # IntegrityError = "this write would break a rule you declared".
    # The database refuses the row rather than storing something broken.
    print(f"  BLOCKED - IntegrityError: {error}")

after = conn.execute("SELECT COUNT(*) FROM expenses").fetchone()[0]
print(f"Expenses after the rejected insert: {after}   (nothing was added)")

conn.close()
