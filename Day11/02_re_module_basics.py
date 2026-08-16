"""
02_re_module_basics.py - The three re functions

TEACHES : findall (get every match, as a list), search (get the first
          match, as an object with .group() and .start()), and sub
          (replace matches, returning a new string). That is 90% of regex.
SLIDE   : Day 11, Slide 6 - Regex, The re Module (deck page 06/20)
RUN     : python 02_re_module_basics.py

EXPECTED OUTPUT IN THE TERMINAL
        Text: Call 9876543210 or 9123456789

        1. re.findall -> ['9876543210', '9123456789']   (a list of str)
        2. re.search  -> <re.Match object ...>
             .group() -> '9876543210'
             .start() -> 5
           No match at all returns None, not an empty object.
        3. re.sub     -> Call XXXXXXXXXX or XXXXXXXXXX
           The original text is unchanged: strings are immutable.
"""

import re

text = "Call 9876543210 or 9123456789"
print(f"Text: {text}\n")

# Every pattern in this file is a RAW string - r'...' rather than '...'.
# In a normal Python string, \d is not a recognised escape, so Python
# leaves it alone today but warns about it and may stop doing so. In a raw
# string the backslash is simply a backslash, which is what regex wants.
# Get in the habit now: if it is a pattern, it gets an r in front.
phone_pattern = r"\d{10}"


def find_all_phones(source: str) -> list[str]:
    """re.findall - every match, as a list of strings."""
    # Returns [] when nothing matches, never None. So it is always safe to
    # loop over or call len() on the result.
    return re.findall(phone_pattern, source)


def find_first_phone(source: str) -> re.Match | None:
    """re.search - the first match, as a Match object (or None)."""
    # search does NOT return the string. It returns an object that also
    # knows WHERE the match was, which findall throws away.
    return re.search(phone_pattern, source)


def mask_phones(source: str) -> str:
    """re.sub - replace every match, returning a new string."""
    return re.sub(phone_pattern, "XXXXXXXXXX", source)


# --- 1. findall ---------------------------------------------------------
phones = find_all_phones(text)
print(f"1. re.findall -> {phones}   ({type(phones).__name__} of {type(phones[0]).__name__})")

# --- 2. search ----------------------------------------------------------
match = find_first_phone(text)
print(f"2. re.search  -> {match}")
# ALWAYS check for None before using the result. search returns None when
# nothing matched, and None has no .group() - the most common regex crash.
if match:
    print(f"     .group() -> {match.group()!r}   (the matched text)")
    print(f"     .start() -> {match.start()}   (where it starts in the string)")

missing = re.search(r"\d{15}", text)
print(f"   Searching for 15 digits -> {missing}   (None, not an empty match)")

# --- 3. sub -------------------------------------------------------------
masked = mask_phones(text)
print(f"3. re.sub     -> {masked}")
print(f"   Original text is unchanged: {text}")
# re.sub returns a NEW string. Python strings are immutable, so nothing
# can edit `text` in place - if you do not assign the result, the work is
# thrown away. A very common first-day mistake.

print("\nWHICH ONE DO I WANT?")
print("  findall - I need every match          -> a list")
print("  search  - I need the first, or just   -> a Match object, or None")
print("            to know whether one exists")
print("  sub     - I want to change the text   -> a new string")
