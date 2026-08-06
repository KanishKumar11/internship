"""
05_container_demo.py - Layout primitive 05a of 05: st.container

TEACHES : Out-of-order rendering. st.container() reserves a SPOT on the page
          immediately, but you can fill that spot later in the script. The
          content still appears at the reserved position, not where it was
          written.
SLIDE   : Day 5, Slide 10 (left side - st.container)
RUN     : streamlit run 05_container_demo.py

EXPECTED OUTPUT IN THE BROWSER
    Three lines, in this order:
        This renders ABOVE 'first'.
        Even though it is defined later in the script.
        This renders first.
    The last line of code appears at the TOP because the container was
    placed there before it was filled.
"""

import streamlit as st

st.title("Container Demo")

# Reserve a position on the page. Nothing is drawn here yet.
holder = st.container()

# This line executes first and is written to the page below the holder.
st.write("This renders first.")

# Now we fill the reserved position - the output jumps ABOVE the line above.
with holder:
    st.write("This renders ABOVE 'first'.")
    st.write("Even though it is defined later in the script.")

# Rare in beginner apps. Common in chat UIs (Day 13), where you reserve the
# message area before you know what the messages will be.
