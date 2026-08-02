"""
16_run_all.py — instructor sanity check (not shown on any slide).

Teaches: nothing — this one is for you. Run it before the session to confirm
files 03, 08, 11 and 15 all still work on this machine.

Note: `import 03_clean_price` is a syntax error, because Python module names
cannot start with a digit. importlib.import_module() takes the name as a
string, which sidesteps that — worth mentioning if a student asks.

Expected output: one summary line per demo, then the success line.
"""

import importlib
import os

clean_price_module = importlib.import_module("03_clean_price")
extract_year_module = importlib.import_module("08_extract_year_solution")
pitfalls_module = importlib.import_module("11_pitfalls_demo")
contacts_module = importlib.import_module("15_clean_contacts_solution")

print("03_clean_price          ->", clean_price_module.clean_price("Rs. 499"),
      "|", clean_price_module.clean_price("FREE"))

print("08_extract_year         ->", extract_year_module.extract_year("2026-07-29"))

print("11_pitfalls_demo        -> running all five demos (output suppressed below)")
print("-" * 60)
pitfalls_module.pitfall_01_mutable_default()
pitfalls_module.pitfall_02_eq_vs_is()
pitfalls_module.pitfall_03_slicing()
pitfalls_module.pitfall_04_string_comparison()
pitfalls_module.pitfall_05_close_twice()
print("-" * 60)

# Resolve the contacts file next to this script, so it works from any folder.
contacts_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "13_contacts.txt")
contacts = contacts_module.clean_contacts(contacts_path)
print(f"15_clean_contacts       -> {len(contacts)} contacts parsed")

print("\n[OK] All demos ran successfully")
