"""
05_status_codes_demo.py - HTTP status codes, triggered for real

TEACHES : What 200, 400 and 404 actually look like coming back from a
          live API, and that the status code is the first thing to read
          when a call does not do what you expected.
SLIDE   : Day 12, Slide 8 - Status Codes table (deck page 08/16)
RUN     : python 05_status_codes_demo.py

EXPECTED OUTPUT IN THE TERMINAL
        200  OK - Use the data
             a valid request for Amritsar
             -> temperature 26.4 C
        404  Not Found - Wrong URL/endpoint
             /v1/nonexistent is not a real endpoint
             -> {"reason":"Not Found","error":true}
        400  Bad Request - Check your params
             latitude=999 is not a real latitude
             -> Latitude must be in range of -90 to 90. Given: 999.0.
        Then a SURPRISE section: calling Open-Meteo with no params at all
        returns 200 with an empty body, not the 400 you would expect.

REQUIRES
    pip install requests, plus an internet connection.

NOTE
    This file does NOT use raise_for_status(), because its whole job is
    to look at bad status codes rather than turn them into exceptions.
    Every other file in this folder uses it.
"""

import requests

URL = "https://api.open-meteo.com/v1/forecast"

# The codes from the slide. In practice you will meet 200, 404 and 429
# constantly, 400 while you are still getting the params right, and 500
# when the API itself is having a bad day.
STATUS_MESSAGES: dict[int, str] = {
    200: "OK - Use the data",
    400: "Bad Request - Check your params",
    401: "Unauthorized - API key missing or invalid",
    403: "Forbidden - You do not have access",
    404: "Not Found - Wrong URL/endpoint",
    429: "Too Many Requests - Rate limited, slow down",
    500: "Server Error - The API is broken, try later",
}


def describe(status_code: int) -> str:
    """Turn a status code into something a human can act on."""
    # The first digit is the category: 2xx worked, 4xx you got it wrong,
    # 5xx the server got it wrong. That alone tells you who has to fix it.
    return STATUS_MESSAGES.get(status_code, f"Unrecognised code ({status_code})")


def try_call(label: str, url: str, params: dict) -> None:
    """Make a call, print its status code and a snippet of the body."""
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"{response.status_code}  {describe(response.status_code)}")
        print(f"     {label}")

        if response.status_code == 200:
            data = response.json()
            temperature = data.get("current", {}).get("temperature_2m")
            print(f"     -> temperature {temperature} C")
        else:
            # On a failure the body usually explains WHY, in a sentence.
            # Read it before you start guessing at the params.
            print(f"     -> {response.text[:100]}")
    except requests.exceptions.Timeout:
        print(f"---  Request timed out - {label}")
    except requests.exceptions.ConnectionError:
        print(f"---  Could not connect - {label}")
    except Exception as error:
        print(f"---  Error - {label}: {error}")
    print()


# --- 200: everything is fine --------------------------------------------
try_call(
    "a valid request for Amritsar",
    URL,
    {"latitude": 31.63, "longitude": 74.87, "current": "temperature_2m"},
)

# --- 404: the endpoint does not exist -----------------------------------
# The classic typo in the URL path. The server is reachable and answers
# perfectly well - it just has nothing at that address.
try_call(
    "/v1/nonexistent is not a real endpoint",
    "https://api.open-meteo.com/v1/nonexistent",
    {"latitude": 31.63, "longitude": 74.87, "current": "temperature_2m"},
)

# --- 400: the params are wrong ------------------------------------------
# The endpoint is right, the request arrived, but 999 is not a latitude.
# 400 means "you sent me something I cannot work with" - and a good API
# says exactly what, as Open-Meteo does here.
try_call(
    "latitude=999 is not a real latitude",
    URL,
    {"latitude": 999, "longitude": 74.87, "current": "temperature_2m"},
)

# --- The surprise -------------------------------------------------------
# You would expect no params at all to be the most obvious 400 of the lot.
# Open-Meteo returns 200 with an empty body instead.
print("SURPRISE - calling with NO params at all")
try:
    empty_response = requests.get(URL, timeout=10)
    print(f"  status {empty_response.status_code}, body is {len(empty_response.text)} characters")
    print("  A 200 with nothing in it. raise_for_status() would NOT catch this,")
    print("  because as far as HTTP is concerned the call succeeded.")
    print("  Lesson: a 200 means the request was valid, NOT that the data is there.")
    print("  Check the data too - which is what the `if data and 'current' in data`")
    print("  guard in the exercise solution is for.")
except requests.exceptions.RequestException as error:
    print(f"  Failed: {error}")
