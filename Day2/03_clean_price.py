"""
03_clean_price.py — anatomy of a function (pairs with Slide 5).

Teaches: the six parts of a real function — the def keyword, the name, the
typed parameters, the docstring, the body (with a guard clause), and the return.
Each part is labelled with a comment below.

Expected output: five "input -> output" lines showing messy price text turned
into usable floats.
"""


# PART 1: def keyword    PART 2: name    PART 3: parameters with type hints
def clean_price(text: str) -> float:
    # PART 4: docstring — what it does, what it takes, what it gives back.
    """Turn messy price text into a number.

    Args:
        text: Raw price text such as "Rs. 499" or "1,299.00".

    Returns:
        The price as a float, or 0.0 if the text contains no digits at all.
    """
    # PART 5: body — and it opens with a GUARD CLAUSE.
    # Handle the bad case first and leave early, so the rest of the function
    # can assume it is working with sane input.
    has_a_digit = False
    for character in text:
        if character.isdigit():
            has_a_digit = True
    if not has_a_digit:
        return 0.0

    # Keep only the characters that can belong to a number.
    # Walk the text one character at a time, and build up a new string
    # containing only the digits and the decimal point.
    kept_characters = ""
    for character in text:
        if character.isdigit() or character == ".":
            kept_characters += character

    # "Rs. 499" leaves a stray leading dot behind, which float() would misread
    # as 0.499. Stripping dots off both ends is enough at this teaching scale.
    cleaned_text = kept_characters.strip(".")

    # PART 6: return — hand the value back to the caller.
    return float(cleaned_text)


if __name__ == "__main__":
    sample_prices = ["Rs. 499", "$12.50", "FREE", "1,299.00", ""]
    for sample in sample_prices:
        print(f"{sample!r:>12}  ->  {clean_price(sample)}")
