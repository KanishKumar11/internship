"""
22_expense_tracker_extended.py - The three extensions

TEACHES : The three extension ideas from the deck, each one a new SQL verb
          in the app - DELETE ... WHERE id = ?, SELECT ... WHERE
          category = ?, and GROUP BY feeding st.bar_chart.
SLIDE   : Day 10, Slide 17 - Exercise Extend (deck page 17/18)
RUN     : streamlit run 22_expense_tracker_extended.py

EXPECTED OUTPUT IN THE BROWSER
    The file-21 app plus a sidebar with a category filter, a coral bar
    chart of spending per category, and a Delete button on every row of
    the table.
    Pick "Food" in the sidebar: the metric, the chart and the table all
    narrow to Food. Delete a row and it disappears from the database
    permanently - the row count in the caption drops by one.

WARNING
    The delete button really deletes. Reset the database at any time with
    python 15_sqlite_full_pattern.py.

ONLY OPEN THIS AFTER FILE 21 WORKS. Core app first, extensions second.
"""

import sqlite3
from contextlib import closing
from pathlib import Path

import pandas as pd
import streamlit as st

DB_FILE = Path(__file__).with_name("expenses.db")

CATEGORIES = ["Food", "Transport", "Books", "Rent", "Entertainment", "Other"]

# The deck's brand palette.
COLOR_CORAL = "#FF6B5B"
COLOR_PRIMARY = "#2A3284"

# The sentinel for "do not filter". A plain string is fine here because it
# is compared in Python, never sent to SQL.
ALL_CATEGORIES = "All"


def init_db() -> None:
    """Create the expenses table if it does not exist yet."""
    with closing(sqlite3.connect(DB_FILE)) as conn:
        with conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    date TEXT NOT NULL,
                    note TEXT
                )
                """
            )


def add_expense(amount: float, category: str, date: str, note: str) -> None:
    """INSERT one expense."""
    with closing(sqlite3.connect(DB_FILE)) as conn:
        with conn:
            conn.execute(
                "INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)",
                (amount, category, date, note),
            )


# --- EXTENSION 1: delete by id ------------------------------------------
def delete_expense(expense_id: int) -> None:
    """DELETE one expense, by primary key."""
    with closing(sqlite3.connect(DB_FILE)) as conn:
        with conn:
            # WHERE id = ? is not optional. DELETE FROM expenses with no
            # WHERE empties the entire table, with no undo and no warning.
            conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))


# --- EXTENSION 2: filter by category ------------------------------------
def get_expenses(category: str = ALL_CATEGORIES) -> pd.DataFrame:
    """SELECT expenses, optionally narrowed to one category."""
    with closing(sqlite3.connect(DB_FILE)) as conn:
        if category == ALL_CATEGORIES:
            return pd.read_sql_query("SELECT * FROM expenses ORDER BY id DESC", conn)
        # Two separate query strings, chosen by an if - NOT one string with
        # the WHERE clause glued on by an f-string. The category value
        # itself still travels as a ? parameter.
        return pd.read_sql_query(
            "SELECT * FROM expenses WHERE category = ? ORDER BY id DESC",
            conn,
            params=(category,),  # read_sql_query takes params, same as execute
        )


def get_total(category: str = ALL_CATEGORIES) -> float:
    """SELECT SUM(amount), for one category or all of them."""
    with closing(sqlite3.connect(DB_FILE)) as conn:
        if category == ALL_CATEGORIES:
            result = conn.execute("SELECT SUM(amount) FROM expenses").fetchone()
        else:
            result = conn.execute(
                "SELECT SUM(amount) FROM expenses WHERE category = ?", (category,)
            ).fetchone()
    # None when nothing matched - a filter that selects an empty category
    # hits this on every rerun.
    return result[0] or 0.0


# --- EXTENSION 3: the chart, aggregated in SQL --------------------------
def get_category_totals() -> pd.DataFrame:
    """SELECT category, SUM(amount) GROUP BY category."""
    with closing(sqlite3.connect(DB_FILE)) as conn:
        return pd.read_sql_query(
            """
            SELECT category, SUM(amount) AS total
            FROM expenses
            GROUP BY category
            ORDER BY total DESC
            """,
            conn,
        )


def get_used_categories() -> list[str]:
    """SELECT DISTINCT category - the options for the sidebar filter."""
    with closing(sqlite3.connect(DB_FILE)) as conn:
        rows = conn.execute(
            "SELECT DISTINCT category FROM expenses ORDER BY category"
        ).fetchall()
    # Build the dropdown from what is actually IN the table, not from the
    # CATEGORIES constant - filtering to a category with no rows would
    # just show an empty table.
    return [row[0] for row in rows]


st.title("Expense Tracker (SQLite) - Extended")

init_db()

with st.sidebar:
    st.write("**Add an expense**")
    with st.form("add_expense_form", clear_on_submit=True):
        amount = st.number_input("Amount (Rs)", min_value=0.0, step=10.0, key="input_amount")
        category = st.selectbox("Category", CATEGORIES, key="input_category")
        date = st.date_input("Date", key="input_date").isoformat()
        note = st.text_input("Note (optional)", key="input_note")
        submitted = st.form_submit_button("Add Expense")

    if submitted:
        if amount <= 0:
            st.error("Amount must be greater than 0.")
        else:
            add_expense(amount, category, date, note)
            st.success(f"Added Rs {amount:,.2f} to {category}.")

    # --- EXTENSION 2, the control ---------------------------------------
    st.write("---")
    st.write("**Filter**")
    filter_options = [ALL_CATEGORIES] + get_used_categories()
    selected_category = st.selectbox("Category", filter_options, key="filter_category")

# The filter feeds the metric and the table together, so the whole page
# always describes the same set of rows.
st.metric(
    "Total Spent" if selected_category == ALL_CATEGORIES else f"Total - {selected_category}",
    f"Rs {get_total(selected_category):,.2f}",
)

filtered_expenses = get_expenses(selected_category)

if filtered_expenses.empty:
    st.info("No expenses to show. Add one from the sidebar.")
else:
    # --- EXTENSION 3, the chart -----------------------------------------
    # Always the full breakdown, not the filtered one: the chart is what
    # you look at to decide WHICH category to filter by, so narrowing it to
    # the current filter would leave a single bar and no comparison.
    st.write("**Spending by Category** (all categories)")
    st.bar_chart(get_category_totals(), x="category", y="total", color=COLOR_CORAL)

    st.write(f"**Expenses** - {len(filtered_expenses)} rows")

    # --- EXTENSION 1, one delete button per row -------------------------
    # st.dataframe cannot hold buttons, so the table is drawn by hand: one
    # st.columns row per expense, with the button in the last column.
    header = st.columns([1, 2, 2, 2, 3, 2])
    for column, title in zip(header, ["ID", "Date", "Category", "Amount", "Note", ""]):
        column.write(f"**{title}**")

    for row in filtered_expenses.itertuples():
        cols = st.columns([1, 2, 2, 2, 3, 2])
        cols[0].write(str(row.id))
        cols[1].write(row.date)
        cols[2].write(row.category)
        cols[3].write(f"Rs {row.amount:,.2f}")
        cols[4].write(row.note if row.note else "-")
        # THE KEY MATTERS. Every widget in a Streamlit app needs a unique
        # key, and these buttons are generated in a loop - so the key has
        # to include something unique per row. The database id is perfect:
        # it never repeats, even after other rows are deleted. Use the loop
        # counter instead and deleting row 2 makes row 3 inherit its key,
        # which makes the wrong row vanish on the next click.
        if cols[5].button("Delete", key=f"delete_{row.id}"):
            delete_expense(row.id)
            # Rerun so the table, metric and chart are all rebuilt from the
            # database without the deleted row. Without this the row stays
            # on screen until the next interaction.
            st.rerun()

    st.caption(f"Showing {len(filtered_expenses)} of {len(get_expenses())} expenses.")
