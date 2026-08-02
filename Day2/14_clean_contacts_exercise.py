"""
14_clean_contacts_exercise.py — closing exercise (pairs with Slide 16: Exercise Brief).

=============================== THE BRIEF ===============================
Write a function:

    def clean_contacts(filepath: str) -> list[tuple[str, str]]:

It should:
  1. Open the file with `with open(...)` and read its lines.
  2. Skip blank lines.
  3. Skip separator lines made of dashes ("---").
  4. Split each line on the FIRST comma only — names may not, but emails
     sometimes do, contain extra text after them.
  5. Skip any line whose email part has no "@" in it.
  6. Return a list of (name, email) tuples, both stripped of stray spaces.
  7. Wrap the open() in try/except FileNotFoundError and return [] on failure.

Expected result for 13_contacts.txt — 5 contacts:
    ('Aarav',   'aarav@example.com')
    ('Priya',   'priya@example.com')
    ('Rahul',   'rahul@college.edu')
    ('Vikram',  'vikram@example.com')
    ('Sanjana', 'sanjana@example.com')
Meera is dropped — she has no email.
========================================================================
"""

CONTACTS_FILE = "13_contacts.txt"


# ------------------------- YOUR CODE HERE -------------------------
def clean_contacts(filepath: str) -> list[tuple[str, str]]:
    """Read a contacts file and return a list of (name, email) tuples."""
    pass  # delete this line and write the real function
# ------------------------------------------------------------------


if __name__ == "__main__":
    contacts = clean_contacts(CONTACTS_FILE)
    print(f"Found {len(contacts) if contacts else 0} contacts:")
    for name, email in contacts or []:
        print(f"  {name:<10} {email}")
