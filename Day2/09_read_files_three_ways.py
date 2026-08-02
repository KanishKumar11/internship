"""
09_read_files_three_ways.py — reading files (pairs with Slide 10: Reading Files — Three Ways).

Teaches: read() gives you one big string, readlines() gives you a list of lines,
and looping over the file object gives you one line at a time without ever
holding the whole file in memory. All three use `with`, so the file closes itself.

Expected output: the file is created, then three labelled sections of output,
then the file is deleted again.
"""

import os

POEM_FILE = "poem.txt"

POEM_TEXT = """The lamp still burns in the hostel hall,
where notes lie open on the table.
Outside, the neem tree keeps its shade,
and morning waits behind the wall.
Someone hums a half-known song,
someone types a broken line,
and the file, at last, compiles.
"""

# Set the file up so this demo is self-contained.
with open(POEM_FILE, "w", encoding="utf-8") as poem_file:
    poem_file.write(POEM_TEXT)
print(f"Created {POEM_FILE}\n")

# WAY 1 — read(): the entire file as a single string.
print("--- WAY 1: f.read() -- one big string ---")
with open(POEM_FILE, "r", encoding="utf-8") as poem_file:
    whole_text = poem_file.read()
print(f"Characters: {len(whole_text)}")
print(f"Lines:      {len(whole_text.splitlines())}\n")

# WAY 2 — readlines(): a list of strings, one per line (newline still attached).
print("--- WAY 2: f.readlines() -- a list of lines ---")
with open(POEM_FILE, "r", encoding="utf-8") as poem_file:
    all_lines = poem_file.readlines()
for line_number, line in enumerate(all_lines, start=1):
    print(f"{line_number}: {line.rstrip()}")
print()

# WAY 3 — loop over the file: one line at a time, nothing else held in memory.
# This is the one to reach for when the file is bigger than your RAM.
print("--- WAY 3: for line in f -- line by line ---")
with open(POEM_FILE, "r", encoding="utf-8") as poem_file:
    for line_number, line in enumerate(poem_file, start=1):
        word_count = len(line.split())
        print(f"Line {line_number}: {word_count} words")

# Clean up so the folder looks the same after the demo as before it.
os.remove(POEM_FILE)
print(f"\nDeleted {POEM_FILE}")
