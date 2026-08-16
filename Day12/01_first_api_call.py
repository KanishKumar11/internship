"""
01_first_api_call.py - Your first API call, in four lines

TEACHES : The pattern every API call in this course follows - call the
          URL with params, check the status code, parse the JSON, use the
          data. Live weather for Amritsar, from the internet, right now.
SLIDE   : Day 12, Slide 6 - Hands-On, The 4-Line Pattern (deck page 06/16)
RUN     : python 01_first_api_call.py

EXPECTED OUTPUT IN THE TERMINAL
        Status code: 200
        Temperature: 28.4 C
        Wind speed : 12.1 km/h
    The numbers change every time you run it - that is the point. This is
    live data, not a file on your laptop.

REQUIRES
    pip install requests
    An internet connection. Open-Meteo is free and needs no API key.
"""

import requests

# The endpoint - the URL the API listens on. Everything that changes from
# call to call goes in params, not in this string.
URL = "https://api.open-meteo.com/v1/forecast"

# Amritsar. Open-Meteo works anywhere on earth; you just give it a point.
AMRITSAR_LAT = 31.63
AMRITSAR_LON = 74.87

try:
    # 1. CALL THE API.
    #    params is a dict; requests turns it into ?latitude=31.63&... for
    #    you. timeout=10 means "give up after 10 seconds" - without it a
    #    dead server can hang this script forever.
    response = requests.get(
        URL,
        params={
            "latitude": AMRITSAR_LAT,
            "longitude": AMRITSAR_LON,
            "current": "temperature_2m,wind_speed_10m",
        },
        timeout=10,
    )

    # 2. CHECK IT WORKED.
    #    200 means OK. raise_for_status() turns any 4xx or 5xx into an
    #    exception, so the code below only runs on a good response.
    print(f"Status code: {response.status_code}")
    response.raise_for_status()

    # 3. PARSE THE JSON.
    #    The API sends back text. .json() turns it into a Python dict -
    #    the same job as json.loads() from Day 9, done for you.
    data = response.json()

    # 4. USE THE DATA.
    #    Navigate the nested dict. The shape comes from the API's docs;
    #    file 08 shows how to work it out for any API.
    temperature = data["current"]["temperature_2m"]
    wind_speed = data["current"]["wind_speed_10m"]

    print(f"Temperature: {temperature} C")
    print(f"Wind speed : {wind_speed} km/h")

except requests.exceptions.RequestException as error:
    # Slide 6 shows this call with no error handling, to keep the four
    # lines visible. Slide 8 puts it back - and every file from 04 onwards
    # uses the full version with one except block per failure mode.
    print(f"The API call failed: {error}")
