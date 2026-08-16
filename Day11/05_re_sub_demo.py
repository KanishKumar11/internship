"""
05_re_sub_demo.py - re.sub: cleaning and transforming text

TEACHES : The four sub patterns from the slide - normalise whitespace,
          strip punctuation, mask sensitive numbers, and reorder text with
          capture groups (\\1, \\2). The cleaning step every text pipeline
          needs before the analysis step.
SLIDE   : Day 11, Slide 11 - Regex, re.sub (deck page 11/20)
RUN     : python 05_re_sub_demo.py

EXPECTED OUTPUT IN THE TERMINAL
    Four before/after pairs:
        1. 'Hello,  World!  This   has   extra   spaces.'
           -> 'Hello, World! This has extra spaces.'
        2. -> 'Hello  World  This   has   extra   spaces'
        3. 'Call 9876543210 for details' -> 'Call XXXXXXXXXX for details'
        4. 'Doe, John' -> 'John Doe'
    Then a combined example: whitespace + punctuation + lowercase, which
    is the standard pre-processing for Day 13's AI exercises.
"""

import re


def show(number: int, label: str, before: str, after: str) -> None:
    """Print one before/after pair."""
    print(f"{number}. {label}")
    print(f"   before: {before!r}")
    print(f"   after : {after!r}\n")


# --- 1. Normalise whitespace -------------------------------------------
# \s matches any whitespace - space, tab, newline. \s+ matches a RUN of it.
# Replacing each run with a single space collapses "   " to " " and also
# turns line breaks into spaces, which is what you want after pulling text
# out of a PDF.
messy_spacing = "Hello,  World!  This   has   extra   spaces."
show(1, "Normalise whitespace - re.sub(r'\\s+', ' ', text)",
     messy_spacing, re.sub(r"\s+", " ", messy_spacing))

# --- 2. Remove punctuation ---------------------------------------------
# [^\w\s] reads as "not a word character and not whitespace" - which is
# everything left over: commas, full stops, exclamation marks. Replacing
# them with '' deletes them.
# Note it does NOT tidy the spacing: removing "," from "Hello," leaves the
# two spaces that followed it. Cleaning steps compose; see the end.
show(2, "Remove punctuation - re.sub(r'[^\\w\\s]', '', text)",
     messy_spacing, re.sub(r"[^\w\s]", "", messy_spacing))

# --- 3. Mask sensitive data ---------------------------------------------
# The same \d{10} from file 02, used to redact rather than to find. This
# is what you do to a phone number or an Aadhaar number before writing it
# to a log file.
sensitive = "Call 9876543210 for details"
show(3, "Mask phone numbers - re.sub(r'\\d{10}', 'XXXXXXXXXX', text)",
     sensitive, re.sub(r"\d{10}", "XXXXXXXXXX", sensitive))

# --- 4. Reorder with capture groups -------------------------------------
# The pattern captures two words either side of a comma. In the
# REPLACEMENT string, \1 and \2 mean "whatever group 1 and group 2
# matched" - so \2 \1 writes them back in the opposite order.
#
# The replacement is a raw string too: r'\2 \1'. Without the r, Python
# would read \2 as an escape sequence before re ever sees it.
name = "Doe, John"
show(4, "Swap name order - re.sub(r'(\\w+), (\\w+)', r'\\2 \\1', text)",
     name, re.sub(r"(\w+), (\w+)", r"\2 \1", name))

# --- Putting them together ----------------------------------------------
# The real pre-processing pipeline: strip punctuation, collapse the
# whitespace that leaves behind, lowercase, trim the ends. Day 13's
# similarity work starts from text in exactly this shape.
raw = "  Hello,  World!  This   has   extra   spaces.  "
cleaned = re.sub(r"[^\w\s]", "", raw)      # punctuation out
cleaned = re.sub(r"\s+", " ", cleaned)     # runs of space -> one space
cleaned = cleaned.strip().lower()          # ends trimmed, case flattened

print("COMBINED - the standard clean-up before any text analysis")
print(f"   raw    : {raw!r}")
print(f"   cleaned: {cleaned!r}")
print("\n   Order matters: punctuation first, THEN whitespace. Do it the")
print("   other way round and the gaps left by the deleted commas are")
print("   still there.")
