"""
02_response_object.py - What comes back from requests.get()

TEACHES : The Response object is not the data - it is an envelope. Six
          attributes worth knowing: status_code, text, json(), headers,
          url and elapsed.
SLIDE   : Day 12, Slide 6 - The Response Object panel (deck page 06/16)
RUN     : python 02_response_object.py

EXPECTED OUTPUT IN THE TERMINAL
        1. status_code : 200
        2. text[:200]  : {"latitude":31.625,"longitude":74.875,...
        3. json()      : <class 'dict'> with keys [...]
        4. content-type: application/json; charset=utf-8
        5. url         : https://api.open-meteo.com/v1/forecast?latitude=...
        6. elapsed     : 0.42 seconds
    Note in 5 that the URL contains the params - requests built that
    string from the dict.

REQUIRES
    pip install requests, plus an internet connection.
"""

import requests

URL = "https://api.open-meteo.com/v1/forecast"

try:
    response = requests.get(
        URL,
        params={
            "latitude": 31.63,
            "longitude": 74.87,
            "current": "temperature_2m,wind_speed_10m",
        },
        timeout=10,
    )
    response.raise_for_status()

    # --- 1. status_code - did it work? ---------------------------------
    # An integer, not a string. 200 is OK; slide 8 has the full table.
    print(f"1. status_code : {response.status_code}")

    # --- 2. text - the raw body, as a string ---------------------------
    # This is literally what came down the wire. Useful when .json()
    # fails: printing .text shows you whether the server sent HTML (an
    # error page) instead of the JSON you expected.
    print(f"2. text[:200]  : {response.text[:200]}")

    # --- 3. json() - the body, parsed into Python ----------------------
    # Note the brackets: json is a METHOD, not an attribute. Writing
    # response.json without them gives you the function object itself,
    # which is a confusing bug to stare at.
    data = response.json()
    print(f"3. json()      : {type(data)} with keys {list(data.keys())}")

    # --- 4. headers - metadata about the response ----------------------
    # A dict-like object, and unusually its keys are case-insensitive:
    # 'content-type' and 'Content-Type' both work.
    print(f"4. content-type: {response.headers['content-type']}")

    # --- 5. url - the address that was actually requested --------------
    # The params dict, assembled into a query string. Print this whenever
    # an API returns something unexpected - it shows exactly what you
    # asked for, which is often not what you thought you asked for.
    print(f"5. url         : {response.url}")

    # --- 6. elapsed - how long the round trip took ---------------------
    # A timedelta. Worth watching: a call that takes 3 seconds will make
    # a Streamlit app feel broken, which is why file 06 caches the result.
    print(f"6. elapsed     : {response.elapsed.total_seconds():.2f} seconds")

except requests.exceptions.Timeout:
    print("Request timed out.")
except requests.exceptions.ConnectionError:
    print("Could not connect. Is the internet working?")
except requests.exceptions.HTTPError as error:
    print(f"API returned an error: {error.response.status_code}")
except Exception as error:
    print(f"Something went wrong: {error}")
