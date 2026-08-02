"""
06_returns_none_fix.py — the fix (pairs with Slide 7: Returns — Why None Will Bite You).

Teaches: change print() to return, and the value becomes usable. Same function
name as 05, one word different in the body, and every caller suddenly works.

Expected output: the greeting, the uppercased greeting, and the greeting joined
onto more text.
"""


def greet(name: str) -> str:
    """Build a greeting and hand it back to the caller.

    Args:
        name: The person's name.

    Returns:
        The greeting string, e.g. "Hello, Aarav!"
    """
    return f"Hello, {name}!"


message = greet("Aarav")

print(message)                              # the caller decides to print it
print(message.upper())                      # and can also transform it
print(message + " Welcome to Day 2.")       # and combine it with other text
