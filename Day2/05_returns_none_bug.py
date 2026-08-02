"""
05_returns_none_bug.py — the None bug (pairs with Slide 7: Returns — Why None Will Bite You).

Teaches: a function that only prints gives the caller nothing back. Python fills
the gap with None, and the crash lands later — at the line that USES the value,
not at the line that produced it.

Expected output: the greeting is printed, then the AttributeError is caught and
explained under a "WHAT WENT WRONG" heading.
"""


def greet(name: str) -> None:
    """Print a greeting and return nothing.

    Args:
        name: The person's name.

    Returns:
        None — the greeting goes to the screen and is then lost.
    """
    print(f"Hello, {name}!")


# The function ran and we saw output, so it FEELS like it worked...
message = greet("Aarav")

# ...but `message` is None, and None has no .upper() method.
try:
    print(message.upper())
except AttributeError as error:
    print("\n--- WHAT WENT WRONG ---")
    print(f"Python said: {error}")
    print("greet() printed the text but never returned it, so message is None.")
    print("The crash is on the .upper() line, but the bug is inside greet().")
