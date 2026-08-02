"""
07_extract_year_exercise.py — mini-exercise (pairs with Slide 8).

=============================== THE BRIEF ===============================
Write a function called extract_year that takes a date string and returns
the year as an int.

    def extract_year(date_str: str) -> int:

Examples:
    extract_year("2026-07-29")        # -> 2026
    extract_year("1999-01-01")        # -> 1999
    extract_year("2020/12/31")        # -> 2020

Assume the year is always the FIRST four digits in the string.
Hint: a list comprehension can pull out just the digit characters.
========================================================================

Expected output right now: five FAIL lines. Your job is to turn them all green.
"""


# ------------------------- YOUR CODE HERE -------------------------
def extract_year(date_str: str) -> int:
    """Return the year found in a date string."""
    pass  # delete this line and write the real function
# ------------------------------------------------------------------


if __name__ == "__main__":
    test_cases: list[tuple[str, int]] = [
        ("2026-07-29", 2026),
        ("1999-01-01", 1999),
        ("2020/12/31", 2020),
        ("2015-03-08 10:45", 2015),
        ("Joined on 2010-06-15", 2010),
    ]
    for date_text, expected_year in test_cases:
        actual_year = extract_year(date_text)
        result_label = "PASS" if actual_year == expected_year else "FAIL"
        print(f"[{result_label}] {date_text!r:<24} expected {expected_year}, got {actual_year}")
