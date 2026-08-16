"""
18_pandas_sqlite_bridge.py - pandas + SQLite: the one-function bridge

TEACHES : pd.read_sql_query (SQL -> DataFrame, no fetchall, no loop) and
          df.to_sql (DataFrame -> table, many rows in one call), plus the
          judgement call: which work belongs in SQL and which in pandas.
SLIDE   : Day 10, Slide 10 - Concept, pandas + SQLite (deck page 10/18)
RUN     : python 18_pandas_sqlite_bridge.py

EXPECTED OUTPUT IN THE TERMINAL
        1. read_sql_query -> a DataFrame
           a DataFrame of shape (3, 5), with real column names
        2. It is a normal DataFrame - every Day 6 tool works
           mean 416.67 | max 680.00 | describe() on amount
        3. to_sql(..., if_exists="append") -> 2 rows in one call
           5 rows now
        4. Let SQL do the aggregating
           GROUP BY in SQL -> a 3-row DataFrame (Food 950, Books 680,
           Transport 420), ready to hand straight to st.bar_chart
        5. Cleanup -> back to 3 rows

    The ids of the appended rows depend on how many rows the table has
    ever held - AUTOINCREMENT never reuses a number - so do not be
    surprised if they are not 4 and 5.

REQUIRES
    expenses.db - run 15_sqlite_full_pattern.py first.
    Leaves the table exactly as it found it (3 rows), so it is safe to
    re-run before class.
"""

import sqlite3
from pathlib import Path

import pandas as pd

DB_FILE = Path(__file__).with_name("expenses.db")

# --- 1. SQL -> DataFrame ------------------------------------------------
# Without pandas this is: execute, fetchall, then rebuild the column names
# from cursor.description to get a DataFrame. read_sql_query does all of
# it, and gets the column names from the database itself.
conn = sqlite3.connect(DB_FILE)
expenses = pd.read_sql_query("SELECT * FROM expenses", conn)
conn.close()

print("1. read_sql_query -> a DataFrame")
print(f"   type: {type(expenses)}  shape: {expenses.shape}")
print(expenses.to_string(index=False))

# --- 2. It is an ordinary DataFrame -------------------------------------
# Nothing about it remembers it came from SQL. Every Day 6 method applies.
print("\n2. It is a normal DataFrame - every Day 6 tool works")
print(f"   mean {expenses['amount'].mean():.2f} | max {expenses['amount'].max():.2f}")
print(expenses["amount"].describe().to_string())

# --- 3. DataFrame -> SQL ------------------------------------------------
new_expenses = pd.DataFrame(
    {
        "amount": [500.0, 300.0],
        "category": ["Food", "Transport"],
        "date": ["2026-08-05", "2026-08-05"],
        "note": ["Dinner", "Auto"],
    }
)

conn = sqlite3.connect(DB_FILE)
# if_exists="append" adds the rows. The default is "fail", which raises
# because the table already exists, and "replace" DROPS the table and
# rebuilds it - which would silently destroy every existing expense. Of
# the three, "replace" is the one to be careful with.
#
# index=False stops pandas writing the DataFrame's 0,1,2 index as an extra
# column. Leave it out and you get a stray "index" column in the table.
#
# Note there is no id column here: it is AUTOINCREMENT, so SQLite fills it.
new_expenses.to_sql("expenses", conn, if_exists="append", index=False)
conn.commit()

after = pd.read_sql_query("SELECT * FROM expenses ORDER BY id", conn)
print(f"\n3. to_sql(..., if_exists=\"append\") -> {len(new_expenses)} rows in one call")
print(f"   {len(after)} rows now")
print(after.to_string(index=False))

# --- 4. Let SQL do the aggregating --------------------------------------
# Both of these give the same answer:
#   pandas: df.groupby("category")["amount"].sum()
#   SQL:    SELECT category, SUM(amount) ... GROUP BY category
# The SQL version reads 4 summary rows out of the database instead of
# pulling every expense into memory first. On 5 rows it makes no
# difference; on 5 million it is the difference between instant and dead.
by_category = pd.read_sql_query(
    """
    SELECT category, SUM(amount) AS total
    FROM expenses
    GROUP BY category
    ORDER BY total DESC
    """,
    conn,
)
print("\n4. Let SQL do the aggregating")
print(by_category.to_string(index=False))
# AS total names the column. Without it the column would be called
# "SUM(amount)", which is awkward to reference and ugly in a chart legend.
# This DataFrame goes straight into st.bar_chart - see file 22.

# --- 5. Clean up so the file is safe to re-run --------------------------
conn.execute("DELETE FROM expenses WHERE note IN (?, ?)", ("Dinner", "Auto"))
conn.commit()
final_count = conn.execute("SELECT COUNT(*) FROM expenses").fetchone()[0]
conn.close()
print(f"\n5. Cleanup -> back to {final_count} rows")

# THE DIVISION OF LABOUR
#   Reading  -> pandas (read_sql_query). One line, real column names.
#   Writing  -> raw SQL with ? placeholders. You control exactly what goes
#               in, and you get an error if it breaks a constraint.
#   Filtering and aggregating -> SQL, if the table is large; pandas, if you
#               already have the DataFrame in hand.
