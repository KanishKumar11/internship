"""
02_greet_after.py — the "after" refactor (pairs with Slide 4: Why Functions, Properly).

Teaches: the same logic as 01, but wrapped in a function that RETURNS a string.
Because it returns instead of prints, the caller decides where the text goes —
which is why the same function serves three completely different input sources.

Expected output: three greeting lines, one per input source (the second one
waits for you to type a name).
"""


def greet(name: str) -> str:
    """Build a greeting for one person.

    Args:
        name: The person's name.

    Returns:
        A greeting string, e.g. "Hello, Aarav!"
    """
    return f"Hello, {name}!"


# Source 1 — a value hardcoded in the file.
student_name = "Aarav"
print(greet(student_name))

# Source 2 — a value typed in at runtime.
typed_name = input("Enter your name: ")
print(greet(typed_name))

# Source 3 — a value pulled out of a list.
# Same function, zero changes. That is the whole point.
class_roll = ["Priya", "Rahul", "Meera"]
print(greet(class_roll[0]))
