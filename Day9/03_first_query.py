"""
03_first_query.py - Your first SQL query

TEACHES : The five-step pattern that every database script in this course
          repeats - connect, cursor, execute, fetchall, close. Everything
          after today is a variation on these five lines.
SLIDE   : Day 9, Slide 15 - Your First SQL Query (deck page 15/25)
RUN     : python 03_first_query.py

EXPECTED OUTPUT IN THE TERMINAL
        (1, 'Aarav', 20, 'Amritsar', 'BCA', 85)
        (2, 'Priya', 21, 'Jalandhar', 'BCA', 92)
        (3, 'Rahul', 22, 'Amritsar', 'BSc-IT', 78)
        (4, 'Meera', 20, 'Ludhiana', 'BCA', 88)
        ... 8 rows in total, one tuple per student.

REQUIRES
    students.db - run 02_create_students_db.py first.
"""

import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).with_name("students.db")

# 1. Connect to the database. This opens the file (and would create an
#    empty one if it were missing - which is why a typo in the filename
#    gives you "no such table" rather than "no such file").
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# 2. Write a SQL query. To Python this is just a string - the database is
#    what understands it. SELECT * means "every column".
cursor.execute("SELECT * FROM students")

# 3. Fetch the results. execute() ran the query; fetchall() is what pulls
#    the rows back into Python, as a list of tuples.
rows = cursor.fetchall()

# 4. Print them. Each tuple is one row, in the column order of the table:
#    (id, name, age, city, branch, marks).
for row in rows:
    print(row)

# 5. Close. Releases the file. The cursor dies with the connection.
conn.close()
