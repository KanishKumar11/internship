"""
04_error_handling.py - The four ways an API call fails

TEACHES : timeout=, raise_for_status(), and one except block per failure
          mode - demonstrated by deliberately breaking the call three
          different ways and catching each one.
SLIDE   : Day 12, Slide 8 - Pattern, Error Handling (deck page 08/16)
RUN     : python 04_error_handling.py

EXPECTED OUTPUT IN THE TERMINAL
        1. A CALL THAT WORKS
           Temperature: 26.4 C
        2. A BAD URL (404)
           API returned an error: 404
        3. AN IMPOSSIBLE TIMEOUT (timeout=0.001)
           Request timed out. Check your internet.
        All three handled. The script finished normally.
    Nothing crashes. That is the whole point - the errors are real, and
    the script still reaches its last line.

REQUIRES
    pip install requests, plus an internet connection.
"""

import requests

URL = "https://api.open-meteo.com/v1/forecast"
AMRITSAR_PARAMS = {
    "latitude": 31.63,
    "longitude": 74.87,
    "current": "temperature_2m",
}


def fetch_weather(url: str, params: dict, timeout: float = 10) -> dict | None:
    """Call an API safely. Returns the parsed JSON, or None if it failed."""
    try:
        # RULE 1: always set a timeout. Without it requests will wait
        # forever for a server that has stopped answering, and your app
        # hangs with no error and no way out.
        response = requests.get(url, params=params, timeout=timeout)

        # RULE 2: always check the status. raise_for_status() turns any
        # 4xx or 5xx into an HTTPError. Without it, a 404 response sails
        # on to .json() and fails later with a confusing message about
        # the JSON being invalid.
        response.raise_for_status()

        return response.json()

    # RULE 3: wrap it in try/except, one block per failure mode - because
    # "the server is slow" and "the URL is wrong" need different fixes.
    #
    # ORDER MATTERS HERE. requests.ConnectTimeout inherits from BOTH
    # ConnectionError and Timeout, so whichever of those two you write
    # first is the one that catches it. Timeout goes first: a connection
    # that timed out is more usefully described as a timeout.
    except requests.exceptions.Timeout:
        print("   Request timed out. Check your internet.")
    except requests.exceptions.ConnectionError:
        print("   Could not connect. Is the internet working?")
    except requests.exceptions.HTTPError as error:
        # The response object survives on the exception, so the status
        # code is still available to report.
        print(f"   API returned an error: {error.response.status_code}")
    except Exception as error:
        # The catch-all. Anything unforeseen - a JSON decode failure, a
        # bug in this file - lands here instead of crashing the program.
        print(f"   Something went wrong: {error}")

    return None


# --- 1. A call that works -----------------------------------------------
print("1. A CALL THAT WORKS")
data = fetch_weather(URL, AMRITSAR_PARAMS)
if data:
    print(f"   Temperature: {data['current']['temperature_2m']} C")

# --- 2. A bad URL -------------------------------------------------------
# /v1/nonexistent is not an endpoint, so Open-Meteo answers 404. Without
# raise_for_status() this would look like a success until .json() choked.
print("\n2. A BAD URL (404)")
bad_data = fetch_weather("https://api.open-meteo.com/v1/nonexistent", AMRITSAR_PARAMS)
print(f"   Returned: {bad_data}  <- None, so the caller knows it failed")

# --- 3. An impossible timeout -------------------------------------------
# A thousandth of a second is not enough to reach a server on the other
# side of the internet, so this always fails - a reliable way to see the
# timeout branch run without unplugging anything.
print("\n3. AN IMPOSSIBLE TIMEOUT (timeout=0.001)")
timeout_data = fetch_weather(URL, AMRITSAR_PARAMS, timeout=0.001)
print(f"   Returned: {timeout_data}")

print("\nAll three handled. The script finished normally.")

# THE THREE RULES
#   1. Always set timeout=.
#   2. Always call raise_for_status() (or check status_code yourself).
#   3. Always wrap the call in try/except.
# Skip any one of them and the app crashes in front of whoever is using
# it - which, on demo day, is the whole room.
