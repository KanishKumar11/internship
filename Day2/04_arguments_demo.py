"""
04_arguments_demo.py — positional, keyword and default arguments (pairs with Slide 6).

Teaches: three ways to pass values into a function, and why keyword arguments
free you from remembering parameter order.

Expected output: labelled lines showing each function called several different
ways, including two calls that look different but mean exactly the same thing.
"""


def add(first_number: int, second_number: int) -> int:
    """Add two numbers passed by position.

    Args:
        first_number: The left-hand number.
        second_number: The right-hand number.

    Returns:
        The sum of the two numbers.
    """
    return first_number + second_number


def greet(name: str, greeting: str) -> str:
    """Build a greeting from an explicit name and greeting word.

    Args:
        name: The person's name.
        greeting: The word to greet them with, e.g. "Namaste".

    Returns:
        The full greeting, e.g. "Namaste, Priya!"
    """
    return f"{greeting}, {name}!"


def greet_default(name: str, greeting: str = "Hello") -> str:
    """Build a greeting, falling back to "Hello" when none is given.

    Args:
        name: The person's name.
        greeting: Optional greeting word; defaults to "Hello".

    Returns:
        The full greeting string.
    """
    return f"{greeting}, {name}!"


if __name__ == "__main__":
    print("--- POSITIONAL: order is the meaning ---")
    print("add(2, 3)        ->", add(2, 3))
    print("add(3, 2)        ->", add(3, 2))

    print("\n--- KEYWORD: name the parameter, forget the order ---")
    print('greet("Priya", "Namaste")                    ->', greet("Priya", "Namaste"))
    print('greet(name="Priya", greeting="Namaste")      ->', greet(name="Priya", greeting="Namaste"))
    # Same result as the line above, with the arguments written back to front.
    print('greet(greeting="Namaste", name="Priya")      ->', greet(greeting="Namaste", name="Priya"))

    print("\n--- DEFAULT: skip it and the fallback fills in ---")
    print('greet_default("Rahul")                       ->', greet_default("Rahul"))
    print('greet_default("Rahul", "Welcome")            ->', greet_default("Rahul", "Welcome"))
    print('greet_default("Rahul", greeting="Welcome")   ->', greet_default("Rahul", greeting="Welcome"))
