"""Closing Exercise — Unit Converter (starting scaffold, YOU fill the TODOs).

Pairs with: Slide 15 (exercise opens) and Slide 16 (the brief + this scaffold)
Teaches:    The shape of every Streamlit app you will ever build:
            read widget values -> branch on them -> render output.
Run it:     streamlit run 06_converter_exercise.py
Expected:   Right now: a dropdown, a number box, and a result that is always 0.00
            because the conversions are not written yet. After you finish the
            TODOs: the result updates live as you type or change the dropdown.

-------------------------------------------------------------------------------
THE BRIEF (10 minutes)
  Build an app that lets the user pick a conversion category (Length, Weight, or
  Temperature), enter a value, and see the converted result live.

  Requirements
    - st.selectbox     to pick the category: ["Length", "Weight", "Temperature"]
    - st.number_input  for the value to convert
    - st.write         to show the result

  Conversion factors (use these exactly)
    Length       1 m  = 3.281 ft
    Weight       1 kg = 2.205 lb
    Temperature  F    = C * 9/5 + 32

  By the end: one category working is fine. Two is good. All three is excellent.
-------------------------------------------------------------------------------
"""

import streamlit as st

# Note: no `if __name__ == "__main__":` block here. That guard exists to stop code
# running when a file is imported. Streamlit already runs this file top to bottom
# as the main script on every interaction, so the guard would only get in the way.

st.title("Unit Converter")

# 1. Pick the category. Passing a list of options means it defaults to the first
#    one, so `category` is never None on the very first render.
category = st.selectbox(
    "What do you want to convert?",
    ["Length", "Weight", "Temperature"],
)

# 2. Get the value. value=0.0 makes it a float input rather than an int input.
value = st.number_input("Enter a value:", value=0.0)

# 3. Branch on the category and compute. `result` and `unit` are set in every
#    branch so that step 4 always has something to show.
if category == "Length":
    # TODO: convert metres to feet (1 m = 3.281 ft)
    result = 0.0
    unit = "feet"
elif category == "Weight":
    # TODO: convert kilograms to pounds (1 kg = 2.205 lb)
    result = 0.0
    unit = "pounds"
else:  # Temperature
    # TODO: convert Celsius to Fahrenheit (F = C * 9/5 + 32)
    result = 0.0
    unit = "degrees Fahrenheit"

# 4. Show the result. :.2f rounds to two decimal places for display.
st.write(f"Result: {result:.2f} {unit}")
