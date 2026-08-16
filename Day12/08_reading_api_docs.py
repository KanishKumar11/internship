"""
08_reading_api_docs.py - The four questions to ask of any API's docs

TEACHES : You will never memorise endpoints. You will read the docs, find
          four things - base URL, required params, authentication,
          response structure - and write the call. Demonstrated by
          walking into an Open-Meteo response one key at a time.
SLIDE   : Day 12, Slide 11 - Skill, Reading API Docs (deck page 11/16)
RUN     : python 08_reading_api_docs.py

EXPECTED OUTPUT IN THE TERMINAL
        STEP 1 - THE BASE URL      https://api.open-meteo.com/v1/forecast
        STEP 2 - REQUIRED PARAMS   latitude, longitude, current
        STEP 3 - AUTHENTICATION    none
        STEP 4 - RESPONSE STRUCTURE
        (the full JSON, pretty-printed)
        Then the navigation, one layer at a time:
          data                        -> dict with 9 keys
          data["current"]             -> dict with 5 keys
          data["current"]["temperature_2m"] -> 26.4  (<class 'float'>)
        And a units lookup showing where "C" comes from.

REQUIRES
    pip install requests, plus an internet connection.
"""

import json

import requests

# --- STEP 1: THE BASE URL -----------------------------------------------
# Where do I send the request? Always near the top of any API's docs,
# often labelled "endpoint". Everything variable goes in params.
BASE_URL = "https://api.open-meteo.com/v1/forecast"
print(f"STEP 1 - THE BASE URL      {BASE_URL}")

# --- STEP 2: THE REQUIRED PARAMS ----------------------------------------
# What must I send for this to work at all? The docs mark params required
# or optional. Open-Meteo needs a point on earth and a list of variables.
PARAMS = {
    "latitude": 31.63,   # required
    "longitude": 74.87,  # required
    "current": "temperature_2m,wind_speed_10m,relative_humidity_2m",
}
print(f"STEP 2 - REQUIRED PARAMS   {', '.join(PARAMS.keys())}")

# --- STEP 3: AUTHENTICATION ---------------------------------------------
# Do I need a key? If so, where does it go - a query param, an
# Authorization header, or a cookie? This is the question that decides
# whether you can use an API in a 90-minute workshop at all.
print("STEP 3 - AUTHENTICATION    none - Open-Meteo is free and open")

# --- STEP 4: THE RESPONSE STRUCTURE -------------------------------------
# The docs show a sample response. Better still, fetch one and look.
print("STEP 4 - RESPONSE STRUCTURE\n")

try:
    response = requests.get(BASE_URL, params=PARAMS, timeout=10)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.Timeout:
    print("Request timed out. Check your internet.")
    raise SystemExit(1)
except requests.exceptions.ConnectionError:
    print("Could not connect. Is the internet working?")
    raise SystemExit(1)
except requests.exceptions.HTTPError as error:
    print(f"API returned an error: {error.response.status_code}")
    raise SystemExit(1)
except Exception as error:
    print(f"Something went wrong: {error}")
    raise SystemExit(1)

# json.dumps with indent=2 is the single most useful line in this file.
# A raw response is one unreadable stream of text; this turns it into
# something you can actually navigate with your eyes.
print(json.dumps(data, indent=2))

# --- NAVIGATING IT, ONE LAYER AT A TIME ---------------------------------
# The mistake is jumping straight to data["current"]["temperature_2m"]
# and getting a KeyError with no idea which of the two keys was wrong.
# Walk in one step at a time and you can see exactly where it breaks.
print("\nNAVIGATING THE RESPONSE")
print(f"  data                              -> dict with {len(data)} keys")
print(f"  {list(data.keys())}")

current = data["current"]
print(f"\n  data['current']                   -> dict with {len(current)} keys")
print(f"  {list(current.keys())}")

temperature = current["temperature_2m"]
print(f"\n  data['current']['temperature_2m'] -> {temperature}  ({type(temperature)})")

# --- The bit the docs give you that a sample response does not ----------
# Open-Meteo returns a parallel "current_units" dict saying what each
# number is measured in. Never hard-code "C" - ask the API.
units = data["current_units"]
print("\nUNITS - the API tells you, so you do not have to assume")
for field in ["temperature_2m", "wind_speed_10m", "relative_humidity_2m"]:
    print(f"  {field:<22} {current[field]:>6} {units[field]}")

print("\nFOUR QUESTIONS, ANY API")
print("  1. What is the base URL?")
print("  2. Which params are required?")
print("  3. Do I need a key, and where does it go?")
print("  4. What shape is the response?")
print("Answer those four and you can call an API you have never seen.")
