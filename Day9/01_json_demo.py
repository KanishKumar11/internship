"""
01_json_demo.py - JSON: save Python dicts to a file, load them back

TEACHES : Python's json module - dump/load for files, dumps/loads for
          strings - and why JSON is the right choice for nested data
          (config, settings) where CSV would need a column per field.
SLIDE   : Day 9, Slide 5 - Storage Format 01 of 03, JSON (deck page 05/25)
RUN     : python 01_json_demo.py

EXPECTED OUTPUT IN THE TERMINAL
    Writes config.json next to this file, then reads it back and prints:
        Saved config.json
        app_name  : Expense Tracker
        categories: ['Food', 'Transport', 'Books']
        currency  : INR
        dark_mode : False
    Open config.json afterwards - indent=4 makes it readable by hand,
    which is the whole point of using JSON for settings.
"""

import json
from pathlib import Path

# Path(__file__).with_name() builds the path NEXT TO THIS SCRIPT, not next
# to whatever folder the terminal happens to be sitting in. Without it,
# running "python Day9/01_json_demo.py" from the repo root would write
# config.json into the repo root instead of into Day9.
CONFIG_FILE = Path(__file__).with_name("config.json")


def build_config() -> dict:
    """Return the app settings as a nested Python dict."""
    # Note the shape: a list inside a dict, and a dict inside a dict. This
    # is exactly what CSV cannot store - a CSV row is flat, so "settings"
    # would have to be flattened into settings_currency, settings_dark_mode
    # columns. JSON keeps the nesting as-is.
    return {
        "app_name": "Expense Tracker",
        "version": "1.0",
        "categories": ["Food", "Transport", "Books"],
        "settings": {
            "currency": "INR",
            "dark_mode": False,
        },
    }


def save_config(config: dict) -> None:
    """Write the dict to config.json as formatted JSON."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        # indent=4 pretty-prints it. Without indent you get one long line -
        # valid JSON, but nobody can read or hand-edit it.
        json.dump(config, file, indent=4)


def load_config() -> dict:
    """Read config.json back into a Python dict."""
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


config = build_config()
save_config(config)
print(f"Saved {CONFIG_FILE.name}")

loaded = load_config()

# JSON round-trips the Python types: the list comes back a list, the nested
# dict comes back a dict, and False comes back as a bool (JSON writes it as
# lowercase "false" in the file, and json.load converts it back).
print(f"app_name  : {loaded['app_name']}")
print(f"categories: {loaded['categories']}")
print(f"currency  : {loaded['settings']['currency']}")
print(f"dark_mode : {loaded['settings']['dark_mode']}")

# THE 's' VARIANTS - strings instead of files.
# json.dump/load work with a file. json.dumps/loads work with a str. You
# will need these on Day 11, when a web API hands you a JSON string that
# was never a file:
#
#   text = json.dumps(config)          # dict  -> str
#   print(text)                        # {"app_name": "Expense Tracker", ...}
#   back = json.loads(text)            # str   -> dict
#   print(back["settings"]["currency"])  # INR
#
# Mnemonic: the extra 's' stands for "string".
