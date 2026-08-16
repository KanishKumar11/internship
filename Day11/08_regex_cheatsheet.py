"""
08_regex_cheatsheet.py - All 10 cheatsheet patterns, tested

TEACHES : Run this to see every regex pattern from the Day 11 cheatsheet
          in one place, each against a test string with several matches in
          it - and, for the three patterns that over-match, the case where
          they go wrong.
SLIDE   : Day 11, Slide 15 - Cheatsheet, 10 Patterns (deck page 15/20)
RUN     : python 08_regex_cheatsheet.py

EXPECTED OUTPUT IN THE TERMINAL
    Ten numbered blocks - pattern name, the pattern, the test string, the
    matches - then a WATCH OUT section with three known over-matches:
        - PHONE matches ISO dates
        - POSTAL CODE matches the first 6 digits of a 10-digit phone
        - NUMBER matches the pieces of an IP address
    Every one of the ten prints at least two matches. If any prints [],
    the pattern is broken - fix it before class.
"""

import re

# (number, name, pattern, test string). Every test string deliberately
# contains more than one match, so an empty result is obviously a bug.
PATTERNS: list[tuple[int, str, str, str]] = [
    (
        1,
        "EMAIL",
        r"[\w.+-]+@[\w-]+\.[\w.]+",
        "Write to aarav@gmail.com or priya@yahoo.co.in, cc john.doe+cv@college.edu",
    ),
    (
        2,
        "PHONE (Indian)",
        r"\+?\d[\d\s-]{8,}\d",
        "Call 9876543210, +91 98765 43210 or 91234-56789",
    ),
    (
        3,
        "DATE (YYYY-MM-DD)",
        r"\d{4}-\d{2}-\d{2}",
        "Joined 2026-08-07, reviewed 2023-12-25",
    ),
    (
        4,
        "DATE (DD/MM/YYYY)",
        r"\d{2}/\d{2}/\d{4}",
        "Due 07/08/2026, submitted 25/12/2023",
    ),
    (
        5,
        "URL",
        r"https?://[\w.-]+",
        "See http://example.com and https://www.google.com for details",
    ),
    (
        6,
        "IP ADDRESS",
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",
        "Router 192.168.1.1, gateway 10.0.0.1",
    ),
    (
        7,
        "POSTAL CODE (India)",
        r"\d{6}",
        "Amritsar 143001, New Delhi 110001",
    ),
    (
        8,
        "NUMBER (with decimals)",
        r"\d+\.?\d*",
        "Values 42, 3.14 and 0.5",
    ),
    (
        9,
        "HASHTAG",
        r"#\w+",
        "Learning #Python and #DataScience this week",
    ),
    (
        10,
        "WORD (letters only)",
        r"[a-zA-Z]+",
        "hello Python 123 world",
    ),
]

# Patterns that match things you did not ask for. Each entry is
# (name, pattern, text that fools it, what it should have found).
OVER_MATCHES: list[tuple[str, str, str, str]] = [
    (
        "PHONE",
        r"\+?\d[\d\s-]{8,}\d",
        "Joined 2023-08-15, left 2024-01-20",
        "nothing - those are dates, not phone numbers",
    ),
    (
        "POSTAL CODE",
        r"\d{6}",
        "Call 9876543210",
        "nothing - that is a phone number, not a PIN code",
    ),
    (
        "NUMBER",
        r"\d+\.?\d*",
        "Router 192.168.1.1",
        "nothing useful - it chops an IP address into pieces",
    ),
]


def run_pattern(number: int, name: str, pattern: str, text: str) -> list[str]:
    """Print one cheatsheet entry and return what it matched."""
    matches = re.findall(pattern, text)
    print(f"{number:2}. {name}")
    print(f"    pattern : {pattern}")
    print(f"    text    : {text}")
    print(f"    matches : {matches}")
    if not matches:
        # A cheatsheet entry that finds nothing is worse than no entry -
        # students will copy it and trust it. Make the failure loud.
        print("    *** FOUND NOTHING - this pattern is broken ***")
    print()
    return matches


print("THE 10 PATTERNS\n")
total_matches = 0
for number, name, pattern, text in PATTERNS:
    total_matches += len(run_pattern(number, name, pattern, text))

print(f"{len(PATTERNS)} patterns, {total_matches} matches in total.\n")

print("WATCH OUT - three of these match more than you asked for\n")
for name, pattern, text, expected in OVER_MATCHES:
    print(f"  {name} on {text!r}")
    print(f"    matched : {re.findall(pattern, text)}")
    print(f"    wanted  : {expected}")
    print()

print("None of these are bugs in the patterns - they are the patterns")
print("doing exactly what they say. A pattern describes a SHAPE, and")
print("different kinds of data sometimes share a shape. The fix is always")
print("the same: print the matches, look at them, and tighten the pattern")
print("only as far as your actual data needs.")
