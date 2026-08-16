"""
04_regex_examples.py - The three patterns you will actually use

TEACHES : Email, Indian phone number, and ISO date - the exact three
          patterns the exercise needs, each with a character-by-character
          breakdown and an honest look at what they get wrong.
SLIDE   : Day 11, Slide 10 - Regex, Real Examples (deck page 10/20)
RUN     : python 04_regex_examples.py

EXPECTED OUTPUT IN THE TERMINAL
        1. EMAILS -> ['aarav@gmail.com', 'priya@yahoo.co.in',
                      'john.doe+filter@gmail.com']
        2. PHONES -> ['9876543210', '+91 98765 43210', '91234-56789']
        3. DATES  -> ['2023-08-15', '2024-01-20']
    Then a WATCH OUT section showing the phone pattern matching
    '2023-08-15' - a date, not a phone number.
"""

import re

# --- 1. EMAIL -----------------------------------------------------------
# [\w.+-]+   the username: letters, digits, _ and the . + - that real
#            addresses use (john.doe+filter@...)
# @          a literal @
# [\w-]+     the domain name: gmail, yahoo, college
# \.         a literal dot - escaped, or . would mean "any character"
# [\w.]+     the ending: com, edu, co.in. The dot is INSIDE the class,
#            which is what makes multi-part endings like .co.in work.
EMAIL_PATTERN = r"[\w.+-]+@[\w-]+\.[\w.]+"

email_text = (
    "Email me at aarav@gmail.com or priya@yahoo.co.in, "
    "or john.doe+filter@gmail.com for filtered mail"
)
# The comma after .co.in is deliberate. A comma is not in [\w.], so the
# pattern stops cleanly there. End the sentence with a full stop instead
# and the match comes back as 'priya@yahoo.co.in.' - dot included, because
# [\w.]+ allows dots and cannot tell a TLD dot from a sentence one.
# File 01 shows that happening.
print("1. EMAILS")
print(f"   text    : {email_text}")
print(f"   pattern : {EMAIL_PATTERN}")
print(f"   matches : {re.findall(EMAIL_PATTERN, email_text)}")

# --- 2. INDIAN PHONE NUMBER ---------------------------------------------
# \+?          an optional leading + (for +91)
# \d           must start with a digit
# [\d\s-]{8,}  at least 8 more digits, spaces or dashes - the {8,} is what
#              lets one pattern cover "9876543210", "+91 98765 43210" and
#              "91234-56789" without a separate pattern for each
# \d           must end on a digit, so a trailing space or dash is dropped
PHONE_PATTERN = r"\+?\d[\d\s-]{8,}\d"

phone_text = "Call 9876543210 or +91 98765 43210 or 91234-56789"
print("\n2. PHONES (Indian formats)")
print(f"   text    : {phone_text}")
print(f"   pattern : {PHONE_PATTERN}")
print(f"   matches : {re.findall(PHONE_PATTERN, phone_text)}")

# --- 3. DATE (YYYY-MM-DD) -----------------------------------------------
# \d{4}  exactly four digits (the year)
# -      a literal dash. Outside [] a dash is just a dash.
# \d{2}  exactly two (month)
# -      dash
# \d{2}  exactly two (day)
DATE_PATTERN = r"\d{4}-\d{2}-\d{2}"

date_text = "Joined 2023-08-15, left 2024-01-20"
print("\n3. DATES (YYYY-MM-DD)")
print(f"   text    : {date_text}")
print(f"   pattern : {DATE_PATTERN}")
print(f"   matches : {re.findall(DATE_PATTERN, date_text)}")

# --- WATCH OUT ----------------------------------------------------------
# The phone pattern says "a digit, then 8+ digits/spaces/dashes, then a
# digit". An ISO date is exactly that shape. So it matches dates too.
print("\nWATCH OUT - the phone pattern on a line of dates:")
print(f"   text    : {date_text}")
print(f"   matches : {re.findall(PHONE_PATTERN, date_text)}")
print("   -> both dates came back as 'phone numbers'.")
print("   This is why the exercise takes phones[0]: on a real resume the")
print("   phone is near the top, above any dates. A stricter pattern")
print("   would anchor on \\b and require exactly 10 digits - but then it")
print("   would stop matching '+91 98765 43210'. Every regex trades")
print("   precision against coverage; pick the side your data needs.")

# The date pattern does NOT have the reverse problem - a phone number has
# no dashes in the right places to look like a date.
print(f"\n   For comparison, the date pattern on the phone line: "
      f"{re.findall(DATE_PATTERN, phone_text)}")
