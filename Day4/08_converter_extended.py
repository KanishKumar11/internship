"""Closing Exercise — Unit Converter with all three extensions.

Pairs with: Slide 16 / Slide 17 (Extensions + pitfalls)
Teaches:    Extension 1 - a direction toggle with st.radio (6 conversions, not 3)
            Extension 2 - st.metric instead of st.write (dashboard-style output)
            Extension 3 - a notes panel in st.sidebar (and why it forgets)
Run it:     streamlit run 08_converter_extended.py
Expected:   A dropdown, a direction radio that relabels itself per category, a
            number box, a big metric showing the converted value, and a sidebar
            notes box. Everything updates live.
"""

import streamlit as st

# --- Conversions, both directions -------------------------------------------


def metres_to_feet(metres: float) -> float:
    return metres * 3.281


def feet_to_metres(feet: float) -> float:
    return feet / 3.281


def kilograms_to_pounds(kilograms: float) -> float:
    return kilograms * 2.205


def pounds_to_kilograms(pounds: float) -> float:
    return pounds / 2.205


def celsius_to_fahrenheit(celsius: float) -> float:
    return celsius * 9 / 5 + 32


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Subtract the offset first, then undo the scale - order matters here."""
    return (fahrenheit - 32) * 5 / 9


st.title("Unit Converter")

category = st.selectbox(
    "What do you want to convert?",
    ["Length", "Weight", "Temperature"],
)

# --- EXTENSION 1: direction toggle ------------------------------------------
# The two choices depend on the category, so we pick the option list first and
# then hand it to st.radio. The radio returns the selected string.
if category == "Length":
    directions = ["m -> ft", "ft -> m"]
elif category == "Weight":
    directions = ["kg -> lb", "lb -> kg"]
else:
    directions = ["C -> F", "F -> C"]

direction = st.radio("Which way?", directions, horizontal=True)

value = st.number_input("Enter a value:", value=0.0)

if direction == "m -> ft":
    result, unit = metres_to_feet(value), "ft"
elif direction == "ft -> m":
    result, unit = feet_to_metres(value), "m"
elif direction == "kg -> lb":
    result, unit = kilograms_to_pounds(value), "lb"
elif direction == "lb -> kg":
    result, unit = pounds_to_kilograms(value), "kg"
elif direction == "C -> F":
    result, unit = celsius_to_fahrenheit(value), "F"
else:  # "F -> C"
    result, unit = fahrenheit_to_celsius(value), "C"

# --- EXTENSION 2: st.metric instead of st.write -----------------------------
# st.metric renders a big number under a small label - the same widget dashboards
# use. It only renders; there is no return value to capture.
st.metric(label=direction, value=f"{result:.2f} {unit}")

# --- EXTENSION 3: a notes panel in the sidebar ------------------------------
# st.sidebar is a container: every st.* command works on it, it just renders on
# the left. st.text_area returns the typed string, exactly like st.text_input.
notes = st.sidebar.text_area("Notes - what did you just convert?")

if notes:
    st.sidebar.write("Your note this run:")
    st.sidebar.write(notes)

# Heads up: these notes do NOT build up a history. Every interaction re-runs this
# file from the top, so `notes` only ever holds what is in the box right now.
# Remembering values across runs needs st.session_state - that's Day 5.
st.sidebar.caption("Notes reset on every rerun. st.session_state fixes that on Day 5.")
