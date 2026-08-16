"""
02_expense_tracker_solution.py - The solo challenge: INSTRUCTOR SOLUTION

TEACHES : All five requirements in one file, using Layout 1 (sidebar +
          main) from the deck. Load on startup, append on submit, rerun
          so every panel refreshes from the same DataFrame.
SLIDE   : Day 8, Slide 5 - Layout 1, Sidebar + Main (deck page 05/15)
RUN     : streamlit run 02_expense_tracker_solution.py

EXPECTED OUTPUT IN THE BROWSER
    A sidebar form (amount, category, date, note) and a main area reading
    "Total Spent  Rs 12,450" over a six-bar chart - Rent 4500, Food 3200,
    Books 1800, Entertainment 1150, Other 1000, Transport 800 - and a
    ten-row table of the newest expenses.
    Add an expense of 500: the total becomes 12,950, the matching bar
    grows, and the new row appears on top of the table. Stop the app,
    start it again - it is still there.

NOTE
    Every app in this folder reads and writes the same expenses.csv, so
    demo rows added here show up in files 03-06 too. Restore the original
    24 rows any time with:  git checkout expenses.csv
"""

from pathlib import Path

import pandas as pd
import streamlit as st

CSV_FILE = Path("expenses.csv")
COLUMNS = ["date", "category", "amount", "note"]

# A fixed list, not free text. Free text lets "food", "Food" and "FOOD"
# become three separate bars in the chart - the groupby cannot tell them
# apart, and the breakdown stops meaning anything.
CATEGORIES = ["Food", "Transport", "Books", "Rent", "Entertainment", "Other"]


def load_expenses() -> pd.DataFrame:
    """Read the CSV, or return an empty frame if this is the first run."""
    # The first run happens on every fresh clone of the repo and on every
    # student's laptop. Without this guard pd.read_csv raises
    # FileNotFoundError and the page never renders at all.
    if not CSV_FILE.exists():
        return pd.DataFrame(columns=COLUMNS)
    return pd.read_csv(CSV_FILE)


def save_expense(date, category: str, amount: float, note: str) -> None:
    """Append one expense to the CSV, keeping everything already stored."""
    # Read-modify-write: load what is there, add one row, write it all
    # back. Slower than an append, but it guarantees the header is written
    # exactly once and the column order never drifts.
    new_row = pd.DataFrame(
        [{"date": str(date), "category": category, "amount": amount, "note": note}]
    )
    updated = pd.concat([load_expenses(), new_row], ignore_index=True)
    # index=False, or pandas adds an unnamed 0,1,2... column on every save.
    updated.to_csv(CSV_FILE, index=False)


st.title("My Expense Tracker")

# Load once, at the top. Streamlit reruns the whole file on every click,
# so this is a fresh read of the CSV on every interaction.
df = load_expenses()

# --- Sidebar: the form --------------------------------------------------
# Layout 1: controls on the left, output on the right. The sidebar does
# not scroll with the main area, which is what you want for a form that
# gets used over and over.
with st.sidebar:
    st.write("**Add Expense**")

    # st.form batches the inputs: typing in a field does NOT rerun the
    # script. Nothing happens until the submit button is pressed, so the
    # user fills all four fields and the app saves exactly once.
    with st.form("add_expense", clear_on_submit=True):
        amount = st.number_input("Amount (Rs)", min_value=0.0, step=10.0, key="f_amount")
        category = st.selectbox("Category", CATEGORIES, key="f_category")
        date = st.date_input("Date", key="f_date")
        note = st.text_input("Note (optional)", key="f_note")
        submitted = st.form_submit_button("Add Expense")

    if submitted:
        # Validate before saving. number_input's min_value stops negatives,
        # but 0.0 is still its default - and an expense of zero is a
        # mis-click, not an expense.
        if amount <= 0:
            st.error("Amount must be greater than 0.")
        else:
            save_expense(date, category, amount, note)
            # The metric, chart and table above already ran with the OLD
            # DataFrame. st.rerun() restarts the script so all three
            # re-read the CSV and show the row that was just added.
            st.rerun()

# --- Empty state --------------------------------------------------------
# On the very first run there is no total worth showing and nothing to
# chart. Say so and stop; st.stop() ends the run, so nothing below it
# executes and no chart draws an empty box.
if df.empty:
    st.info("No expenses yet. Add your first one from the sidebar.")
    st.stop()

# --- Requirement 3: the total ------------------------------------------
# One prominent number. The :, gives 12,450 instead of 12450, and .0f
# drops the decimals nobody reads on a headline figure.
st.metric("Total Spent", f"Rs {df['amount'].sum():,.0f}")

# --- Requirement 4: spending by category -------------------------------
# Day 6's groupby reduces 24 rows to one number per category; Day 7's
# bar_chart draws it. Chart the summary, never the raw rows - bar_chart
# would otherwise plot 24 separate bars with no labels worth reading.
st.write("**Spending by Category**")
by_category = df.groupby("category")["amount"].sum()
st.bar_chart(by_category)

# --- Requirement 5: recent expenses ------------------------------------
# Newest first, ten rows. The CSV stores ISO dates (2026-08-04), and ISO
# dates sort correctly as plain text - which is the whole reason to store
# them in that format rather than "04 Aug".
st.write("**Recent Expenses**")
recent = df.sort_values("date", ascending=False).head(10)
st.dataframe(recent)
