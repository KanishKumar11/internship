"""
11_form_extended.py - Closing exercise: EXTENDED VERSION

TEACHES : All three extension ideas from slide 15, on top of the basic form:
            1. a Clear button that resets fields via del st.session_state[...]
            2. validation inside `if submitted:` - no summary when invalid
            3. a submission history kept in st.session_state and shown as a
               table - a mini database without a database
SLIDE   : Day 5, Slide 15 (Extensions + pitfalls)
RUN     : streamlit run 11_form_extended.py

EXPECTED OUTPUT IN THE BROWSER
    The Personal Info Form, plus a Clear button underneath. Submitting with
    an empty name or an email without "@" shows a red error and NO summary.
    A valid submit shows the green summary and adds a row to the "Past
    submissions" table at the bottom, which grows with every submit.
"""

import streamlit as st

st.title("Personal Info Form - Extended")


def is_valid_email(email: str) -> bool:
    """A deliberately simple check - enough for a form demo, not for production."""
    return "@" in email


# === EXTENSION 3 (setup) === history list, initialised once per session.
if "submissions" not in st.session_state:
    st.session_state.submissions = []

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

if submitted:
    # === EXTENSION 2 === validate BEFORE showing anything or saving.
    if not user_name.strip():
        st.error("Please enter your name")
    elif not is_valid_email(contact_email):
        st.error("Please enter a valid email")
    else:
        st.success("Form submitted!")
        st.write(f"**Name:** {user_name}")
        st.write(f"**Email:** {contact_email}")
        st.write(f"**Age:** {user_age}")
        st.write(f"**Gender:** {user_gender}")

        # === EXTENSION 3 === append this submission to the history list.
        st.session_state.submissions.append(
            {
                "Name": user_name,
                "Email": contact_email,
                "Age": user_age,
                "Gender": user_gender,
            }
        )

# === EXTENSION 1 === Clear button. Deleting a widget's key removes its stored
# value, so on the next rerun the widget is rebuilt with its default. We call
# st.rerun() so the emptied fields are visible straight away.
if st.button("Clear", key="clear_button"):
    for widget_key in ["user_name", "contact_email", "user_age", "user_gender"]:
        if widget_key in st.session_state:
            del st.session_state[widget_key]
    st.rerun()

# === EXTENSION 3 (display) === show every submission made this session.
st.divider()
st.subheader("Past submissions")

if st.session_state.submissions:
    # st.dataframe accepts a list of dictionaries and renders it as a table.
    st.dataframe(st.session_state.submissions)
else:
    st.caption("Nothing submitted yet. Fill the form above and click Submit.")

# Note: the history lives in session_state, so it is cleared when the browser
# tab is refreshed. Saving to a real file or database comes on Day 6.
