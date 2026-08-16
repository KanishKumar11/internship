"""
03_layout_top_form.py - The same app, Layout 2: top form + dashboard

TEACHES : The no-sidebar variant. The form sits at the top of the main
          area with its widgets side by side in st.columns, and the
          dashboard stacks underneath. Simplest of the four layouts.
SLIDE   : Day 8, Slide 6 - Layout 2, Top Form + Dashboard (deck page 06/15)
RUN     : streamlit run 03_layout_top_form.py

EXPECTED OUTPUT IN THE BROWSER
    A four-field form across the top, then two metric cards side by side -
    "Total Spent  Rs 12,450" and "Aug 2026  Rs 2,610" - then the six-bar
    category chart, then a ten-row table. All in one scrolling column.

NOTE
    Same expenses.csv as the other apps in this folder. The five
    requirements are identical to 02 - only the arrangement changed.
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

# --- The form, across the top ------------------------------------------
# No sidebar in this layout. st.columns(4) inside the form lays the
# widgets out horizontally instead of stacking them, so the whole form is
# one band across the page rather than a tall strip.
with st.form("add_expense", clear_on_submit=True):
    st.write("**Add Expense**")
    c1, c2, c3, c4 = st.columns(4)
    # Call the widget on the column object and it lands in that column.
    amount = c1.number_input("Amount (Rs)", min_value=0.0, step=10.0, key="f_amount")
    category = c2.selectbox("Category", CATEGORIES, key="f_category")
    date = c3.date_input("Date", key="f_date")
    note = c4.text_input("Note (optional)", key="f_note")
    submitted = st.form_submit_button("Add")

if submitted:
    if amount <= 0:
        st.error("Amount must be greater than 0.")
    else:
        save_expense(date, category, amount, note)
        # Everything below re-reads the CSV on the next run.
        st.rerun()

if df.empty:
    st.info("No expenses yet. Add your first one using the form above.")
    st.stop()

# --- Two metrics in a row ----------------------------------------------
# The deck's second card is "this month". Rather than the real calendar
# month - which would read Rs 0 whenever this is run outside August 2026 -
# take the month of the most recent expense, so the card always has data
# to show and the label says which month it means.
dates = pd.to_datetime(df["date"])
latest = dates.max()
this_month = df[(dates.dt.year == latest.year) & (dates.dt.month == latest.month)]

col_total, col_month = st.columns(2)
col_total.metric("Total Spent", f"Rs {df['amount'].sum():,.0f}")
col_month.metric(latest.strftime("%b %Y"), f"Rs {this_month['amount'].sum():,.0f}")

# --- Chart, then table, stacked ----------------------------------------
st.write("**Spending by Category**")
st.bar_chart(df.groupby("category")["amount"].sum())

st.write("**Recent Expenses**")
st.dataframe(df.sort_values("date", ascending=False).head(10))
