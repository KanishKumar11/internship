"""
09_weather_exercise.py - Day 12 exercise: STUDENT SCAFFOLD

TEACHES : Everything from today in one app - a cached API call, full
          error handling, and three metric cards fed by live data.
SLIDE   : Day 12, Slide 13 - Exercise Brief (deck page 13/16)
RUN     : streamlit run 09_weather_exercise.py

EXPECTED OUTPUT IN THE BROWSER
    Right now: the title, a working city dropdown, and a message saying
    get_weather is not written yet.
    Once you finish the TODOs: three cards showing live temperature, wind
    speed and humidity for the city you picked - and they change when you
    switch city.

REQUIRES
    pip install requests streamlit
    An internet connection. Open-Meteo needs no API key.

--------------------------------------------------------------------------
THE BRIEF
    Build a Streamlit app that calls the Open-Meteo API and shows the
    current weather for Amritsar, Delhi or Mumbai.

REQUIREMENTS
    [ ] Call https://api.open-meteo.com/v1/forecast with requests.get()
    [ ] Pass params: latitude, longitude, and
        current=temperature_2m,wind_speed_10m,relative_humidity_2m
    [ ] Wrap the API call in a function decorated @st.cache_data(ttl=600)
    [ ] Handle errors with try/except - timeout, connection, HTTP error
    [ ] Show 3 st.metric cards: Temperature, Wind Speed, Humidity
    [ ] Let the user pick a city with st.selectbox

HOW TO WORK
    Uncomment one TODO at a time, save, and watch the browser reload.
    The dropdown is already wired up; you write the function it feeds.

IF NOTHING APPEARS
    (1) Is the internet on? (2) Is requests installed? (3) Is the URL
    right? (4) Are you passing params= rather than gluing the URL
    together? Those four cover almost every failure.
--------------------------------------------------------------------------
"""

import requests
import streamlit as st

URL = "https://api.open-meteo.com/v1/forecast"

# City name -> (latitude, longitude).
CITIES: dict[str, tuple[float, float]] = {
    "Amritsar": (31.63, 74.87),
    "Delhi": (28.61, 77.21),
    "Mumbai": (19.08, 72.88),
}

st.title("Live Weather Dashboard")


# --- The cached API call ------------------------------------------------
# TODO 1: add the caching decorator on the line directly above the def.
#   Without it, EVERY widget interaction calls the API again - every
#   dropdown change, every click. ttl=600 keeps each answer for 10 min.
# @st.cache_data(ttl=600)
def get_weather(latitude: float, longitude: float) -> dict:
    """Fetch the current weather for one point. Returns {} on failure."""
    # TODO 2: make the call, check it, return the parsed JSON.
    #   Note timeout=10 - without it the app can hang forever.
    # try:
    #     response = requests.get(
    #         URL,
    #         params={
    #             "latitude": latitude,
    #             "longitude": longitude,
    #             "current": "temperature_2m,wind_speed_10m,relative_humidity_2m",
    #         },
    #         timeout=10,
    #     )
    #     response.raise_for_status()
    #     return response.json()

    # TODO 3: handle the failures. Timeout goes FIRST - requests'
    #   ConnectTimeout counts as both a Timeout and a ConnectionError,
    #   so whichever you write first is the one that catches it.
    # except requests.exceptions.Timeout:
    #     st.error("Request timed out. Check your internet.")
    # except requests.exceptions.ConnectionError:
    #     st.error("Could not connect. Is the internet working?")
    # except requests.exceptions.HTTPError as error:
    #     st.error(f"API returned an error: {error.response.status_code}")
    # except Exception as error:
    #     st.error(f"Something went wrong: {error}")

    # Return an empty dict rather than None, so the caller can write
    # `if data` and `data["current"]` without a type check first.
    return {}


# --- The user picks a city - this part is done for you ------------------
city = st.selectbox("Choose a city", list(CITIES.keys()), key="city_select")
latitude, longitude = CITIES[city]
st.caption(f"{city} is at {latitude}, {longitude}")

weather_data = get_weather(latitude, longitude)

# --- Show the results ---------------------------------------------------
# TODO 4: pull the three numbers out of the response and show them.
#   The shape is data["current"]["temperature_2m"] - file 08 walks
#   through the whole response if you want to see it laid out.
#   Guard with `if weather_data and "current" in weather_data` first: a
#   failed call returns {}, and a 200 can still come back empty.
# if weather_data and "current" in weather_data:
#     current = weather_data["current"]
#     temperature = current["temperature_2m"]
#     wind_speed = current["wind_speed_10m"]
#     humidity = current["relative_humidity_2m"]
#
#     TODO 5: three cards side by side. Call .metric() on each column
#       object, not on st, and the card lands inside that column.
#     col1, col2, col3 = st.columns(3)
#     col1.metric("Temperature", f"{temperature} C")
#     col2.metric("Wind Speed", f"{wind_speed} km/h")
#     col3.metric("Humidity", f"{humidity}%")
# else:
#     st.warning("No weather data to show.")

if not weather_data:
    st.info("get_weather() is not written yet - work through the TODOs above.")

# FINISHED EARLY? File 11 has the three extensions: a 7-day forecast, a
# city search by name, and an hourly temperature chart.
