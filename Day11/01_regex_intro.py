"""
01_regex_intro.py - Why regex exists: 20 lines vs 1 line

TEACHES : The same job done twice - find every email in a string by hand,
          then with one call to re.findall - so the point of regex is the
          code you DELETE, not a new syntax to memorise.
SLIDE   : Day 11, Slide 5 - Concept, Regex (deck page 05/20)
RUN     : python 01_regex_intro.py

EXPECTED OUTPUT IN THE TERMINAL
        Text: Contact: aarav@example.com or priya@college.edu

        THE HARD WAY (manual string handling)
          ['aarav@example.com', 'priya@college.edu']
        THE ONE-LINE WAY (regex)
          ['aarav@example.com', 'priya@college.edu']
        Same answer: True

        Now add a comma...
          manual : ['aarav@example.com', 'priya@college.edu']
          regex  : ['aarav@example.com,', 'priya@college.edu.']
    The last block is the honest part: the slide's \\S+ pattern grabs the
    punctuation too. Slide 15's cheatsheet pattern is the fix.
"""

import re

text = "Contact: aarav@example.com or priya@college.edu"
print(f"Text: {text}\n")


def find_emails_by_hand(source: str) -> list[str]:
    """Find emails without regex - split, check, strip, hope."""
    found: list[str] = []
    for word in source.split():
        # Rule 1: an email has an @ in it.
        if "@" not in word:
            continue
        # Rule 2: strip the punctuation that sentences leave attached.
        cleaned = word.strip(",.!?;:")
        # Rule 3: the bit after the @ needs a dot in it, or "aarav@localhost"
        # would count as an email address.
        domain = cleaned.split("@")[-1]
        if "." not in domain:
            continue
        found.append(cleaned)
    return found


def find_emails_with_regex(source: str) -> list[str]:
    """Find emails with one call. This is the whole function."""
    # r'...' is a RAW string: Python leaves the backslashes alone instead of
    # trying to interpret \S as an escape sequence. Every regex in this
    # course is written this way - it is the difference between a pattern
    # that works and one that fails for reasons you cannot see.
    #
    # \S+  one or more non-space characters (the username)
    # @    a literal @
    # \S+  the domain
    # \.   a literal dot - escaped, because a bare . means "any character"
    # \S+  the .com / .edu / .co.in
    return re.findall(r"\S+@\S+\.\S+", source)


manual_result = find_emails_by_hand(text)
regex_result = find_emails_with_regex(text)

print("THE HARD WAY (manual string handling)")
print(f"  {manual_result}")
print("THE ONE-LINE WAY (regex)")
print(f"  {regex_result}")
print(f"Same answer: {manual_result == regex_result}\n")

# --- The part the slide leaves out -------------------------------------
# The two approaches agree on the tidy sentence above. They stop agreeing
# the moment the emails sit inside real punctuation, because \S+ means
# "anything that is not a space" - and a comma is not a space.
messy = "Mail aarav@example.com, then priya@college.edu."
print("Now add a comma...")
print(f"  text   : {messy}")
print(f"  manual : {find_emails_by_hand(messy)}")
print(f"  regex  : {find_emails_with_regex(messy)}")
print("  -> \\S+ swallowed the comma and the full stop.")

# The fix is a stricter pattern - the one on slide 15's cheatsheet, which
# lists exactly which characters are allowed instead of "anything".
strict = re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", messy)
print(f"  strict : {strict}")
print("  -> better, though the trailing dot still sneaks in, because")
print("     [\\w.]+ allows dots. Regex is iteration, not magic.")
