"""Closing Exercise — Unit Converter (instructor's complete solution).

Pairs with: Slide 15 / Slide 16 - reveal this after students have attempted it.
Teaches:    input -> logic -> output, with the logic pulled into small typed
            functions so each conversion can be read (and tested) on its own.
Run it:     streamlit run 07_converter_solution.py
Expected:   Pick a category, type a value, and the result line updates live -
            no button needed, because every keystroke re-runs the script.
"""

import streamlit as st


def metres_to_feet(metres: float) -> float:
    """1 m = 3.281 ft."""
    return metres * 3.281


def kilograms_to_pounds(kilograms: float) -> float:
    """1 kg = 2.205 lb."""
    return kilograms * 2.205


def celsius_to_fahrenheit(celsius: float) -> float:
    """F = C * 9/5 + 32 - note the offset, this one is not a plain factor."""
    return celsius * 9 / 5 + 32


st.title("Unit Converter")

category = st.selectbox(
    "What do you want to convert?",
    ["Length", "Weight", "Temperature"],
)

value = st.number_input("Enter a value:", value=0.0)

if category == "Length":
    result = metres_to_feet(value)
    unit = "feet"
elif category == "Weight":
    result = kilograms_to_pounds(value)
    unit = "pounds"
else:  # Temperature
    result = celsius_to_fahrenheit(value)
    unit = "degrees Fahrenheit"

st.write(f"Result: {result:.2f} {unit}")
