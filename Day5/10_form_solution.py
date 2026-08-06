"""
10_form_solution.py - Closing exercise: INSTRUCTOR SOLUTION

TEACHES : The complete st.form pattern - batch the inputs, read them once on
          submit, render a summary. This is the data-collection shape every
          group will reuse in their Phase 4 project.
SLIDE   : Day 5, Slide 14 (reveal after students have tried 09_form_exercise)
RUN     : streamlit run 10_form_solution.py

EXPECTED OUTPUT IN THE BROWSER
    A bordered form with Name, Email, Age slider, Gender radio and a Submit
    button. Typing changes nothing on screen. Clicking Submit shows a green
    "Form submitted!" banner followed by four summary lines.
"""

import streamlit as st

st.title("Personal Info Form")

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

    submitted = st.form_submit_button("Submit")

# `submitted` is True only on the rerun triggered by the button click.
if submitted:
    st.success("Form submitted!")
    st.write(f"**Name:** {user_name}")
    st.write(f"**Email:** {contact_email}")
    st.write(f"**Age:** {user_age}")
    st.write(f"**Gender:** {user_gender}")
