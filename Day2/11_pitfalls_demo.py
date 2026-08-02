"""
11_pitfalls_demo.py — five pitfalls (pairs with Slide 12: Pitfalls That Will Bite You).

Teaches: five Python behaviours that are not bugs in Python, but reliably become
bugs in student code. Each one gets its own function so you can run them one at
a time in the terminal.

Expected output: five labelled sections, each printing the surprising result
followed by the fix.
"""

import os


def pitfall_01_mutable_default() -> None:
    """Show that a default list is created ONCE and then shared by every call."""

    def add_item(item: int, basket: list[int] = []) -> list[int]:
        """Add an item to a basket. The default value here is the trap."""
        basket.append(item)
        return basket

    # Two calls, each expecting a brand-new empty basket.
    print("First call  add_item(1) ->", add_item(1))
    print("Second call add_item(2) ->", add_item(2))
    print("The 1 is still there: both calls shared the SAME default list.")

    def add_item_fixed(item: int, basket: list[int] | None = None) -> list[int]:
        """Same idea, but a fresh list is built inside the call."""
        if basket is None:
            basket = []
        basket.append(item)
        return basket

    print("FIX: default None, build the list inside ->",
          add_item_fixed(1), add_item_fixed(2))


def pitfall_02_eq_vs_is() -> None:
    """Show the difference between equal values and the same object."""
    list_a = [1, 2, 3]
    list_b = [1, 2, 3]
    list_c = list_a  # not a copy — a second name for the same list

    print("list_a == list_b ->", list_a == list_b, "  (same contents)")
    print("list_a is list_b ->", list_a is list_b, "  (different objects in memory)")
    print("list_a is list_c ->", list_a is list_c, "  (same object, two names)")
    print("Rule: use == for values, use `is` only for None.")


def pitfall_03_slicing() -> None:
    """Show that a slice stops BEFORE its end index."""
    nums = [10, 20, 30, 40, 50]

    print("nums        ->", nums)
    print("nums[1:3]   ->", nums[1:3], "  (index 1 up to but NOT including 3)")
    print("nums[:3]    ->", nums[:3], "  (from the start)")
    print("nums[3:]    ->", nums[3:], "  (to the end)")
    print("nums[-1]    ->", nums[-1], "  (last item, no length arithmetic needed)")


def pitfall_04_string_comparison() -> None:
    """Show that input() always hands back a string, never a number."""
    # Pretend the student typed 18 at an input("Enter your age: ") prompt.
    typed_age = "18"

    print("typed_age        ->", repr(typed_age), "  (a string, always)")
    print("typed_age == 18  ->", typed_age == 18, "  (str never equals int)")

    try:
        print(typed_age > 15)
    except TypeError as error:
        print("typed_age > 15   -> TypeError:", error)

    age = int(typed_age)
    print("FIX: int(typed_age) == 18 ->", age == 18, " and age > 15 ->", age > 15)


def pitfall_05_close_twice() -> None:
    """Show that a closed file cannot be read from, even though the name still exists."""
    temp_file_path = "temp_demo.txt"
    with open(temp_file_path, "w", encoding="utf-8") as temp_file:
        temp_file.write("one line of text\n")

    # Opening without `with` means WE are responsible for closing it.
    file_handle = open(temp_file_path, "r", encoding="utf-8")
    print("While open  ->", file_handle.read().strip())
    file_handle.close()

    # The variable still exists, so this looks legal. It is not.
    try:
        file_handle.read()
    except ValueError as error:
        print("After close -> ValueError:", error)

    print("FIX: use `with open(...)` and never call close() by hand.")
    os.remove(temp_file_path)


if __name__ == "__main__":
    demos: list[tuple[str, object]] = [
        ("PITFALL 1 — Mutable default argument", pitfall_01_mutable_default),
        ("PITFALL 2 — == vs is", pitfall_02_eq_vs_is),
        ("PITFALL 3 — Slicing stops early", pitfall_03_slicing),
        ("PITFALL 4 — input() returns a string", pitfall_04_string_comparison),
        ("PITFALL 5 — Reading a closed file", pitfall_05_close_twice),
    ]
    for title, demo_function in demos:
        print("=" * 60)
        print(title)
        print("=" * 60)
        demo_function()
        print()
