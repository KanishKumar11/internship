"""
03_query_params.py - Query parameters: the dict, not the string

TEACHES : Why you pass params={...} instead of gluing a URL together by
          hand - readability, encoding, and the fact that a dict can be
          built at runtime from whatever the user picked.
SLIDE   : Day 12, Slide 7 - Concept, Query Parameters (deck page 07/16)
RUN     : python 03_query_params.py

EXPECTED OUTPUT IN THE TERMINAL
        BAD  - URL built by hand   -> 26.4 C
        GOOD - params dict         -> 26.4 C
        Same answer: True
        The URL requests built: ...?latitude=31.63&longitude=74.87&...

        DYNAMIC - one function, any city
          Amritsar   31.63, 74.87  ->  26.4 C
          Delhi      28.61, 77.21  ->  29.1 C
          Mumbai     19.08, 72.88  ->  27.8 C

REQUIRES
    pip install requests, plus an internet connection.
"""

import requests

URL = "https://api.open-meteo.com/v1/forecast"

# City name -> (latitude, longitude). This is the dict the exercise and
# every file after it uses.
CITY_COORDS: dict[str, tuple[float, float]] = {
    "Amritsar": (31.63, 74.87),
    "Delhi": (28.61, 77.21),
    "Mumbai": (19.08, 72.88),
}


def temperature_from(response: requests.Response) -> float:
    """Pull the current temperature out of an Open-Meteo response."""
    return response.json()["current"]["temperature_2m"]


# --- THE BAD WAY: build the query string by hand ------------------------
# It works, and that is the trap. It is hard to read, easy to typo, and
# the moment a value comes from a variable you are doing string surgery.
bad_url = "https://api.open-meteo.com/v1/forecast?latitude=31.63&longitude=74.87&current=temperature_2m"
try:
    bad_response = requests.get(bad_url, timeout=10)
    bad_response.raise_for_status()
    bad_temperature = temperature_from(bad_response)
    print(f"BAD  - URL built by hand   -> {bad_temperature} C")
except requests.exceptions.RequestException as error:
    print(f"BAD  - failed: {error}")
    raise SystemExit(1)

# --- THE GOOD WAY: hand requests a dict ---------------------------------
try:
    good_response = requests.get(
        URL,
        params={
            "latitude": 31.63,
            "longitude": 74.87,
            "current": "temperature_2m",
        },
        timeout=10,
    )
    good_response.raise_for_status()
    good_temperature = temperature_from(good_response)
    print(f"GOOD - params dict         -> {good_temperature} C")
except requests.exceptions.RequestException as error:
    print(f"GOOD - failed: {error}")
    raise SystemExit(1)

print(f"Same answer: {bad_temperature == good_temperature}")
print(f"The URL requests built: {good_response.url}")

# Look closely at that URL: the comma in a multi-value param comes back as
# %2C. That is URL encoding, and requests did it without being asked. Do
# it by hand and you have to remember to encode spaces, commas, ampersands
# and anything a user typed - which is where hand-built URLs really break.

# --- WHY THE DICT WINS: params can be built at runtime -----------------
# The whole point. The URL string above is frozen at Amritsar forever; the
# dict below is assembled per call from whatever the user chose.
print("\nDYNAMIC - one function, any city")


def get_temperature(latitude: float, longitude: float) -> float | None:
    """Fetch the current temperature for any point on earth."""
    try:
        response = requests.get(
            URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m",
            },
            timeout=10,
        )
        response.raise_for_status()
        return temperature_from(response)
    except requests.exceptions.Timeout:
        print("  Request timed out.")
    except requests.exceptions.ConnectionError:
        print("  Could not connect.")
    except requests.exceptions.HTTPError as error:
        print(f"  API error: {error.response.status_code}")
    except Exception as error:
        print(f"  Error: {error}")
    # Every except path falls through to here and returns None, so the
    # caller has one thing to check instead of four.
    return None


for city, (latitude, longitude) in CITY_COORDS.items():
    temperature = get_temperature(latitude, longitude)
    reading = f"{temperature} C" if temperature is not None else "unavailable"
    print(f"  {city:<10} {latitude}, {longitude}  ->  {reading}")
