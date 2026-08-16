"""
19_error_demo.py - The five SQL errors you will hit today

TEACHES : How to read a sqlite3 exception - the TYPE names the category,
          the MESSAGE names the exact problem - by triggering each of the
          five on purpose and catching it.
SLIDE   : Day 10, Slide 11 - Debugging, Common SQL Errors (deck page 11/18)
RUN     : python 19_error_demo.py

EXPECTED OUTPUT IN THE TERMINAL
    Six numbered blocks. Each prints the error, then CAUSE and FIX:
        1. OperationalError: no such table: expensive
        2. OperationalError: near "FROM": syntax error
        3. IntegrityError: NOT NULL constraint failed: expenses.amount
        4. ProgrammingError: Incorrect number of bindings supplied ...
        5. Error binding parameter 2: type 'list' is not supported
        6. ProgrammingError: Cannot operate on a closed database.
    Nothing crashes - every error is caught. Ends with "All 6 errors were
    raised and caught on purpose. Nothing is broken."

    TWO NOTES ON SLIDE 11's ERROR 04
    It lists "InterfaceError: Error binding parameter" as the wrong-number-
    of-values error. Two corrections, both shown live here:
      - A wrong COUNT of values raises ProgrammingError ("Incorrect number
        of bindings supplied") - case 4 - not InterfaceError.
      - "Error binding parameter" is the wrong TYPE, not the wrong count -
        case 5. Its class moved: InterfaceError on Python 3.10-3.12,
        ProgrammingError on 3.13+. Case 5 catches both, so the demo prints
        whichever class the machine in the room actually raises.

REQUIRES
    expenses.db - run 15_sqlite_full_pattern.py first.
    Changes nothing: every statement here fails by design.
"""

import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).with_name("expenses.db")


def report(number: int, title: str, error: Exception, cause: str, fix: str) -> None:
    """Print one caught error in a fixed shape: what, why, how to fix."""
    print(f"\n{number}. {title}")
    print(f"   {type(error).__name__}: {error}")
    print(f"   CAUSE: {cause}")
    print(f"   FIX  : {fix}")


conn = sqlite3.connect(DB_FILE)

# --- 1. OperationalError: no such table ---------------------------------
try:
    conn.execute("SELECT * FROM expensive")
except sqlite3.OperationalError as error:
    report(
        1,
        "Querying a table that does not exist",
        error,
        "The table was never created, or the name is misspelled - here "
        "'expensive' instead of 'expenses'.",
        "Run CREATE TABLE IF NOT EXISTS first, and check the spelling. "
        "SQL keywords are case-insensitive, but names must match.",
    )

# --- 2. OperationalError: syntax error ----------------------------------
try:
    # The mistake is the missing column list after SELECT. SQLite reports
    # the position where parsing failed - "near FROM" - which is one token
    # LATER than the actual mistake. Always look at what comes before.
    conn.execute("SELECT FROM expenses WHERE amount > 100")
except sqlite3.OperationalError as error:
    report(
        2,
        "A typo in the SQL string",
        error,
        "A missing comma, quote, bracket or column list. The error names "
        "the token where parsing gave up, not the token that is wrong.",
        "Read the word the error names, then look at what comes BEFORE it. "
        "Here: SELECT has nothing to select.",
    )

# --- 3. IntegrityError: NOT NULL constraint failed ----------------------
try:
    # amount is declared NOT NULL, and None becomes SQL NULL.
    conn.execute(
        "INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)",
        (None, "Food", "2026-08-04", "No amount given"),
    )
except sqlite3.IntegrityError as error:
    report(
        3,
        "Inserting NULL into a NOT NULL column",
        error,
        "A required column got None. In an app this is usually an empty "
        "form field arriving as None or an empty string.",
        "Validate before you INSERT - reject the submit if amount is "
        "missing. Or drop NOT NULL if the field really is optional.",
    )

# --- 4. ProgrammingError: wrong NUMBER of values ------------------------
try:
    # Four ? placeholders, three values in the tuple.
    conn.execute(
        "INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)",
        (250.00, "Food", "2026-08-04"),
    )
except sqlite3.ProgrammingError as error:
    report(
        4,
        "Wrong number of values for the ? placeholders",
        error,
        "The number of ? in the SQL does not match the length of the tuple. "
        "Four ?s, three values.",
        "Count the ?s. Count the values. They must match exactly - and "
        "remember a one-value tuple needs its trailing comma: (value,).",
    )

# --- 5. InterfaceError: wrong TYPE of value -----------------------------
try:
    # A list cannot be stored in a column. SQLite only binds None, int,
    # float, str and bytes - anything else has to be converted first.
    conn.execute(
        "INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)",
        (250.00, ["Food", "Transport"], "2026-08-04", "A list, not a string"),
    )
except (sqlite3.InterfaceError, sqlite3.ProgrammingError) as error:
    # Both are caught because this error changed class between Python
    # versions: InterfaceError on 3.10-3.12, ProgrammingError on 3.13+.
    # The message - "Error binding parameter N" - is the same either way,
    # and the message is the part worth recognising.
    report(
        5,
        "Binding a value of a type SQLite cannot store",
        error,
        "A list, dict, date or custom object was passed as a parameter. "
        "SQLite stores None, int, float, str and bytes - nothing else.",
        "Convert first: str(value) for text, .isoformat() for a date, "
        "json.dumps(value) for a list or dict.",
    )

# --- 6. ProgrammingError: closed database -------------------------------
conn.close()
try:
    conn.execute("SELECT * FROM expenses")
except sqlite3.ProgrammingError as error:
    report(
        6,
        "Using a connection after closing it",
        error,
        "conn.close() ran before this line. Common when close() sits in the "
        "middle of a function, or inside a loop that runs more than once.",
        "Close at the very end of the function, after the last fetch - or "
        "use with closing(sqlite3.connect(...)) as conn (see file 17).",
    )

print("\nAll 6 errors were raised and caught on purpose. Nothing is broken.")

# HOW TO READ ANY sqlite3 ERROR
#   The TYPE is the category:
#     OperationalError - the SQL could not run (bad table, bad syntax)
#     IntegrityError   - the SQL ran but would break a rule you declared
#     ProgrammingError - your Python misused the API (wrong ? count, closed
#                        connection)
#     InterfaceError   - a parameter was of a type SQLite cannot store
#   The MESSAGE names the exact table, column or token. Read the last line
#   of the traceback first - that is where the real error is.
