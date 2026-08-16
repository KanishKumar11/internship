"""
10_weather_solution.py - Day 12 exercise: INSTRUCTOR SOLUTION

TEACHES : The full pattern - user input, a cached API call with complete
          error handling, and three metric cards. The shape of every
          data-fetching app: input -> API call -> display.
SLIDE   : Day 12, Slide 14 - Solution Walkthrough (deck page 14/16)
          Reveal after students have tried file 09.
RUN     : streamlit run 10_weather_solution.py

EXPECTED OUTPUT IN THE BROWSER
    A city dropdown over three cards - Temperature, Wind Speed, Humidity -
    filled with live values for the chosen city, and a caption showing
    the reading's timestamp.
    Switch city and all three update. Switch back within 10 minutes and
    they come from the cache, with no API call at all.

REQUIRES
    pip install requests streamlit
    An internet connection. Open-Meteo needs no API key.
"""

import requests
import streamlit as st

URL = "https://api.open-meteo.com/v1/forecast"

CITIES: dict[str, tuple[float, float]] = {
    "Amritsar": (31.63, 74.87),
    "Delhi": (28.61, 77.21),
    "Mumbai": (19.08, 72.88),
}

# The three variables to ask for, as one comma-separated string - which is
# how Open-Meteo wants them. Named here so the call below stays readable.
CURRENT_FIELDS = "temperature_2m,wind_speed_10m,relative_humidity_2m"


@st.cache_data(ttl=600)
def get_weather(latitude: float, longitude: float) -> dict:
    """Fetch current weather for one point. Returns {} if the call fails.

    Cached for 10 minutes per (latitude, longitude) pair, so switching
    back and forth between cities does not re-hit the API.
    """
    try:
        response = requests.get(
            URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": CURRENT_FIELDS,
            },
            timeout=10,  # never leave this off - it is what stops a hang
        )
        response.raise_for_status()  # 4xx/5xx become exceptions here
        return response.json()

    # Timeout BEFORE ConnectionError: requests' ConnectTimeout subclasses
    # both, so the first matching block wins and a timed-out connection is
    # more usefully reported as a timeout.
    except requests.exceptions.Timeout:
        st.error("Request timed out. Check your internet.")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect. Is the internet working?")
    except requests.exceptions.HTTPError as error:
        st.error(f"API returned an error: {error.response.status_code}")
    except Exception as error:
        st.error(f"Something went wrong: {error}")

    # Every failure path ends here. An empty dict, not None, so the caller
    # has one shape to handle instead of two.
    return {}


st.title("Live Weather Dashboard")

# --- Input --------------------------------------------------------------
city = st.selectbox("City", list(CITIES.keys()), key="city_select")
latitude, longitude = CITIES[city]

# --- API call -----------------------------------------------------------
weather_data = get_weather(latitude, longitude)

# --- Display ------------------------------------------------------------
# Two conditions, not one. `weather_data` catches the failure case, where
# the function returned {}. `"current" in weather_data` catches a 200 that
# came back without the data - which Open-Meteo really can do (file 05).
if weather_data and "current" in weather_data:
    current = weather_data["current"]

    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", f"{current['temperature_2m']} C")
    col2.metric("Wind Speed", f"{current['wind_speed_10m']} km/h")
    col3.metric("Humidity", f"{current['relative_humidity_2m']}%")

    # The API tells you when the reading was taken. Show it - a dashboard
    # of live numbers with no timestamp is a dashboard you cannot trust.
    st.caption(f"Reading taken at {current['time']} ({weather_data['timezone']})")
else:
    st.warning("No weather data to show. See the error above.")

# THE PIPELINE
#   pick a city -> look up coords -> call the cached API -> parse the
#   JSON -> show metrics.
#   Swap the API and this is any data-fetching app you will ever write.
