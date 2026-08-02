"""
01_greet_before.py — the "before" script (pairs with Slide 4: Why Functions, Properly).

Teaches: what semester-1 script-style code looks like, and the three problems
it quietly creates the moment the program grows past 10 lines.

Expected output: prompts for a name, then prints one greeting line.
"""

# PROBLEM 1 — Hard to reuse: greeting a second person means copy-pasting these lines.
name = input("Enter your name: ")

# PROBLEM 2 — Untestable: there is no name to call, so no test can ever check the result.
greeting = "Hello, " + name + "!"

# PROBLEM 3 — Mixes input and output: reading, building and showing are welded together,
# so you cannot use the greeting anywhere except the screen.
print(greeting)
