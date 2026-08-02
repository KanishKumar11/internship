"""
10_write_append_demo.py — writing files (pairs with Slide 11: Writing Files — Modes Cheat-Sheet).

Teaches: the three modes you will actually use.
    'w'  write   — CREATES the file, or WIPES an existing one. There is no undo,
                   no confirmation and no recycle bin. Opening a file with 'w'
                   destroys its contents before you have written a single byte.
    'a'  append  — creates if missing, otherwise adds to the end. Safe for logs.
    'r'  read    — read only; fails if the file does not exist.

Expected output: two lines written, two appended, then all four read back.
"""

import os

LOG_FILE = "log.txt"

# 'w' — start a fresh file. Anything previously in log.txt is gone at this point.
with open(LOG_FILE, "w", encoding="utf-8") as log_file:
    log_file.write("Session start\n")
    log_file.write("Day 2 -- Python, Properly\n")
print(f"Wrote 2 lines to {LOG_FILE} using mode 'w'")

# 'a' — add to the end, leaving the existing two lines untouched.
with open(LOG_FILE, "a", encoding="utf-8") as log_file:
    log_file.write("Closing exercise completed\n")
    log_file.write("Students present: 28\n")
print(f"Appended 2 lines to {LOG_FILE} using mode 'a'")

# 'r' — read it all back to prove what survived.
print(f"\n--- Contents of {LOG_FILE} ---")
with open(LOG_FILE, "r", encoding="utf-8") as log_file:
    print(log_file.read())

os.remove(LOG_FILE)
print(f"Deleted {LOG_FILE}")
