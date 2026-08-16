"""
03_regex_syntax.py - The four building blocks

TEACHES : Anchors (where), quantifiers (how many), character classes
          (what kind), groups (sub-patterns). Every pattern you will ever
          read is a combination of these four.
SLIDE   : Day 11, Slide 9 - Regex, The Vocabulary (deck page 09/20)
RUN     : python 03_regex_syntax.py

EXPECTED OUTPUT IN THE TERMINAL
    Four labelled sections, each printing the pattern, the test string and
    the result. Highlights:
        \\bcat\\b on "cat catch category"      -> ['cat']  (not catch)
        \\d* on "abc"                        -> lots of empty strings
        colou?r on "color colour"           -> ['color', 'colour']
        [^0-9] on "a1b2"                    -> ['a', 'b']
        (\\d{3})-(\\d{4}) on "123-4567"       -> [('123', '4567')]
    That last one is the surprise: with groups, findall returns TUPLES,
    not the whole match.
"""

import re


def show(label: str, pattern: str, text: str) -> None:
    """Print one pattern, its test string, and what it found."""
    matches = re.findall(pattern, text)
    print(f"  {label:<22} {pattern:<16} on {text!r}")
    print(f"  {'':22} -> {matches}")


# --- 1. ANCHORS - WHERE the match has to sit ----------------------------
# Anchors match a POSITION, not a character. They consume nothing; they
# just say "only count a match if it is here".
print("1. ANCHORS - where")
show("^ start of string", r"^Hello", "Hello world")
show("^ (no match)", r"^Hello", "Say Hello world")
show("$ end of string", r"world$", "Hello world")
show("\\b word boundary", r"\bcat\b", "cat catch category")
# Without the \b markers, r'cat' would match inside "catch" and "category"
# too. \b is the line between a word character and a non-word character -
# which is why it is the difference between finding a word and finding a
# fragment of one.
show("no boundary", r"cat", "cat catch category")

# --- 2. QUANTIFIERS - HOW MANY ------------------------------------------
print("\n2. QUANTIFIERS - how many")
show("* zero or more", r"\d*", "a1b22")
# * matching zero of something means it succeeds at EVERY position,
# including the gaps between characters - hence all the empty strings.
# It is almost never what you want on its own; + is.
show("+ one or more", r"\d+", "a1b22")
show("? zero or one", r"colou?r", "color colour")
show("{n} exactly n", r"\d{10}", "9876543210 and 12345")
show("{n,m} n to m", r"\d{2,4}", "1 12 123 12345")
# Note the last one: on "12345" the {2,4} takes the first FOUR digits and
# then matches the leftover "5"? No - it takes 4, then 1 is left, which is
# below the minimum of 2, so it is skipped. Quantifiers are greedy: they
# take as many as they can before giving any back.

# --- 3. CHARACTER CLASSES - WHAT KIND -----------------------------------
print("\n3. CHARACTER CLASSES - what kind")
show(". any char", r"a.c", "abc axc a c")
show("\\d digit", r"\d+", "room 101, floor 2")
show("\\w word char", r"\w+", "hello_123 world!")
show("\\s whitespace", r"\s+", "a b  c")
show("[abc] any of", r"[aeiou]", "regex")
show("[^0-9] NOT these", r"[^0-9]", "a1b2")
# Inside [], a ^ at the FRONT means "not". Anywhere else it is a literal ^.
# The three shorthands have opposites too: \D not-digit, \W not-word,
# \S not-whitespace.

# --- 4. GROUPS - SUB-PATTERNS -------------------------------------------
print("\n4. GROUPS - sub-patterns")
show("() capture group", r"(\d{3})-(\d{4})", "call 123-4567 now")
# THE GOTCHA. The moment a pattern contains (), findall stops returning
# the whole match and returns the GROUPS instead - one tuple per match.
# Useful when you want the pieces; surprising when you did not.
show("no group", r"\d{3}-\d{4}", "call 123-4567 now")
show("| OR", r"cat|dog", "a cat and a dog")
show("(?:) non-capture", r"(?:ab)+", "ababab cd")
# (?:...) groups things for a quantifier WITHOUT capturing them, so findall
# goes back to returning whole matches. Use it when you need the brackets
# for structure, not for extraction.

# re.search keeps both: .group(0) is everything, .group(1) is the first ().
match = re.search(r"(\d{3})-(\d{4})", "call 123-4567 now")
if match:
    print("\n  With re.search you get both:")
    print(f"    .group(0) -> {match.group(0)!r}   (the whole match)")
    print(f"    .group(1) -> {match.group(1)!r}       (first bracket)")
    print(f"    .group(2) -> {match.group(2)!r}      (second bracket)")
