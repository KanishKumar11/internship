"""
09_form_exercise.py - Closing exercise: STARTING SCAFFOLD

TEACHES : st.form batches several inputs into a single submit. Typing in a
          form field does NOT rerun the script - only the submit button does.
SLIDE   : Day 5, Slide 14 (Exercise - Personal Info Form)
RUN     : streamlit run 09_form_exercise.py

EXPECTED OUTPUT IN THE BROWSER (once you finish the TODOs)
    A bordered form with Name, Email, Age slider, Gender radio and a Submit
    button. Clicking Submit shows a success message and a summary of the
    four values. Before the TODOs are done, Submit shows only a reminder.

SOLUTION : 10_form_solution.py (instructor reveals this after the build)

--------------------------------------------------------------------------
THE BRIEF                                                          15 MIN
--------------------------------------------------------------------------
Build a personal info form using st.form that collects:
    * name    -> st.text_input
    * email   -> st.text_input
    * age     -> st.slider, range 0 to 100
    * gender  -> st.radio: Male / Female / Other / Prefer not to say

Requirements:
    [x] Wrap the inputs in `with st.form("personal_info"):`
    [x] Every widget has a UNIQUE, DESCRIPTIVE key
    [x] The form ends with submitted = st.form_submit_button("Submit")
    [ ] On submit, show a summary of all four values (st.write or st.json)

Note on keys: slide 15's pitfall list warns that key="name" is too generic
and collides easily, so we use user_name / contact_email / user_age /
user_gender instead.
--------------------------------------------------------------------------
"""

import streamlit as st

st.title("Personal Info Form")

# 1. Define the form. Everything indented here is submitted together.
with st.form("personal_info"):
    st.write("**Enter your details**")

    user_name = st.text_input("Name", key="user_name")
    contact_email = st.text_input("Email", key="contact_email")
    user_age = st.slider("Age", 0, 100, 20, key="user_age")
    user_gender = st.radio(
        "Gender",
        ["Male", "Female", "Other", "Prefer not to say"],
        key="user_gender",
    )

    # Every st.form needs exactly one submit button. It returns True on the
    # rerun that follows the click, and False on every other rerun.
    submitted = st.form_submit_button("Submit")

# 2. Handle the submit. This block sits OUTSIDE the `with` block.
if submitted:
    # TODO 1: show a success message with st.success("Form submitted!")

    # TODO 2: print the name, e.g. st.write(f"**Name:** {user_name}")

    # TODO 3: print the email

    # TODO 4: print the age

    # TODO 5: print the gender

    # Delete the line below once your TODOs above are written.
    st.info("TODO: build the summary output here.")

# EXTEND PHASE HINT - a Clear button that resets the form:
# if st.button("Clear", key="clear_button"):
#     del st.session_state["user_name"]
#     del st.session_state["contact_email"]
#     st.rerun()
