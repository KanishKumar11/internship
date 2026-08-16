"""
04_layout_tabs.py - The same app, Layout 3: tabs (Add / View / Charts)

TEACHES : One screen per task. st.tabs splits the app into three views so
          each screen holds one job - and shows the catch: every tab's
          code runs on every rerun, whether or not you are looking at it.
SLIDE   : Day 8, Slide 7 - Layout 3, Tabs (deck page 07/15)
RUN     : streamlit run 04_layout_tabs.py

EXPECTED OUTPUT IN THE BROWSER
    Three tabs under the title. "Add Expense" holds the form and nothing
    else. "View Expenses" shows "Total Spent  Rs 12,450" over the full
    24-row sortable table. "Charts" shows the six-bar category chart and a
    line chart of daily spending from 27 Jul to 4 Aug.
    Add an expense on tab 1 - Streamlit returns you to tab 1, and the
    other two tabs are already updated when you click across.

NOTE
    Same expenses.csv as the other apps in this folder.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

CSV_FILE = Path("expenses.csv")
COLUMNS = ["date", "category", "amount", "note"]
CATEGORIES = ["Food", "Transport", "Books", "Rent", "Entertainment", "Other"]


def load_expenses() -> pd.DataFrame:
    """Read the CSV, or return an empty frame if this is the first run."""
    if not CSV_FILE.exists():
        return pd.DataFrame(columns=COLUMNS)
    return pd.read_csv(CSV_FILE)


def save_expense(date, category: str, amount: float, note: str) -> None:
    """Append one expense to the CSV, keeping everything already stored."""
    new_row = pd.DataFrame(
        [{"date": str(date), "category": category, "amount": amount, "note": note}]
    )
    updated = pd.concat([load_expenses(), new_row], ignore_index=True)
    updated.to_csv(CSV_FILE, index=False)


st.title("My Expense Tracker")

df = load_expenses()

# st.tabs returns one container per label. Tabs are NOT pages: the code in
# all three blocks runs on every rerun regardless of which tab is open -
# Streamlit just hides the two you are not looking at. That is why the
# empty-state check has to live inside each tab, not once at the top.
tab_add, tab_view, tab_charts = st.tabs(["Add Expense", "View Expenses", "Charts"])

# --- Tab 1: the form only ----------------------------------------------
with tab_add:
    with st.form("add_expense", clear_on_submit=True):
        st.write("**Add a new expense**")
        amount = st.number_input("Amount (Rs)", min_value=0.0, step=10.0, key="f_amount")
        category = st.selectbox("Category", CATEGORIES, key="f_category")
        date = st.date_input("Date", key="f_date")
        note = st.text_input("Note (optional)", key="f_note")
        submitted = st.form_submit_button("Add")

    if submitted:
        if amount <= 0:
            st.error("Amount must be greater than 0.")
        else:
            save_expense(date, category, amount, note)
            # st.success would flash and vanish on the rerun below, so
            # show the confirmation on the NEXT run instead - park it in
            # session_state here and print it at the bottom of this tab.
            st.session_state["last_added"] = f"Added Rs {amount:,.0f} to {category}."
            st.rerun()

    if "last_added" in st.session_state:
        st.success(st.session_state["last_added"])

# --- Tab 2: the numbers and the table ----------------------------------
with tab_view:
    if df.empty:
        st.info("No expenses yet. Add one on the first tab.")
    else:
        st.metric("Total Spent (all time)", f"Rs {df['amount'].sum():,.0f}")
        st.write("**All Expenses**")
        # The whole table here, not just ten rows - this tab exists to
        # browse. st.dataframe is sortable: click a column header.
        st.dataframe(df.sort_values("date", ascending=False))

# --- Tab 3: the visualisations -----------------------------------------
with tab_charts:
    if df.empty:
        st.info("No expenses yet - nothing to chart.")
    else:
        st.write("**Spending by Category**")
        st.bar_chart(df.groupby("category")["amount"].sum())

        st.write("**Spending Over Time**")
        # groupby("date") collapses the several expenses recorded on one
        # day into a single point, which is what makes the line readable.
        # sort_index() puts the days in order - groupby sorts by default,
        # but being explicit costs nothing and documents the intent.
        st.line_chart(df.groupby("date")["amount"].sum().sort_index())
