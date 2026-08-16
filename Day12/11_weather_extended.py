"""
11_weather_extended.py - The three extensions

TEACHES : The extension ideas from the deck - a 7-day forecast table, any
          city in the world via the geocoding API, and an hourly
          temperature chart. Day 6's DataFrames and Day 7's charts, fed
          by today's API instead of a CSV.
SLIDE   : Day 12, Slide 15 - Exercise, Extend (deck page 15/16)
RUN     : streamlit run 11_weather_extended.py

EXPECTED OUTPUT IN THE BROWSER
    A sidebar where you either pick a preset city or type any city name
    to look up. The main area shows the three current-weather cards, a
    line chart of the next 24 hours, and a 7-day forecast table with
    daily highs and lows.
    Type "Ludhiana" or "Tokyo" in the search box and everything updates.

REQUIRES
    pip install requests streamlit pandas
    An internet connection. Both Open-Meteo endpoints are free, no key.

ONLY OPEN THIS AFTER FILE 10 WORKS. Core dashboard first, extras second.
"""

import pandas as pd
import requests
import streamlit as st

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

CITIES: dict[str, tuple[float, float]] = {
    "Amritsar": (31.63, 74.87),
    "Delhi": (28.61, 77.21),
    "Mumbai": (19.08, 72.88),
    # === EXTENSION 2 (the easy half) === five more preset cities ===
    "Chandigarh": (30.73, 76.78),
    "Jalandhar": (31.33, 75.58),
    "Ludhiana": (30.90, 75.86),
    "Bengaluru": (12.97, 77.59),
    "Kolkata": (22.57, 88.36),
}


@st.cache_data(ttl=600)
def get_weather(latitude: float, longitude: float) -> dict:
    """Current conditions, 24-hour hourly, and a 7-day daily forecast.

    One call fetches all three. Asking for current, hourly and daily
    together is far better than three separate calls - same data, a third
    of the network time, and a single cache entry.
    """
    try:
        response = requests.get(
            FORECAST_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,wind_speed_10m,relative_humidity_2m",
                # === EXTENSION 1 === the 7-day forecast ===
                "daily": "temperature_2m_max,temperature_2m_min",
                # === EXTENSION 3 === hourly data for the chart ===
                "hourly": "temperature_2m",
                "forecast_days": 7,
                # timezone=auto makes the API return local times for the
                # coordinates given. Without it everything comes back in
                # GMT and a chart of "today" starts at the wrong hour.
                "timezone": "auto",
            },
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        st.error("Request timed out. Check your internet.")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect. Is the internet working?")
    except requests.exceptions.HTTPError as error:
        st.error(f"API returned an error: {error.response.status_code}")
    except Exception as error:
        st.error(f"Something went wrong: {error}")
    return {}


# === EXTENSION 2 === look up any city by name ===========================
@st.cache_data(ttl=3600)
def search_city(name: str) -> list[dict]:
    """Turn a city name into coordinates using Open-Meteo's geocoding API.

    A different endpoint from the forecast one, but the same four
    questions from slide 11 answer it: base URL, params (name, count),
    no auth, and results nested under data["results"].
    """
    try:
        response = requests.get(
            GEOCODING_URL,
            params={"name": name, "count": 5},
            timeout=10,
        )
        response.raise_for_status()
        # A search with no hits omits "results" entirely rather than
        # returning an empty list - so .get() with a default, not [...].
        return response.json().get("results", [])
    except requests.exceptions.RequestException as error:
        st.error(f"City search failed: {error}")
        return []


def hourly_next_24(weather_data: dict) -> pd.DataFrame:
    """The next 24 hourly readings, as a DataFrame ready for st.line_chart."""
    hourly = pd.DataFrame(weather_data["hourly"])
    hourly["time"] = pd.to_datetime(hourly["time"])

    # The hourly array starts at midnight today, so roughly half of it is
    # already in the past. Slice from the current reading's timestamp so
    # the chart shows the next 24 hours rather than the last 12.
    now = pd.to_datetime(weather_data["current"]["time"])
    upcoming = hourly[hourly["time"] >= now].head(24)

    # st.line_chart uses the index for the x axis - so put the time there.
    return upcoming.set_index("time")


def daily_table(weather_data: dict) -> pd.DataFrame:
    """The 7-day forecast, tidied up for display."""
    daily = pd.DataFrame(weather_data["daily"])
    daily["time"] = pd.to_datetime(daily["time"]).dt.strftime("%a %d %b")
    # Rename before display: "temperature_2m_max" is what the API calls
    # it, not what a person reading a table wants to see.
    return daily.rename(
        columns={
            "time": "Day",
            "temperature_2m_max": "High (C)",
            "temperature_2m_min": "Low (C)",
        }
    )


st.title("Live Weather Dashboard - Extended")

# --- Sidebar: preset city, or search any city ---------------------------
with st.sidebar:
    st.write("**Location**")
    mode = st.radio("Pick how", ["Preset city", "Search by name"], key="mode_radio")

    if mode == "Preset city":
        city = st.selectbox("City", list(CITIES.keys()), key="city_select")
        latitude, longitude = CITIES[city]
        label = city
    else:
        query = st.text_input("City name", value="Amritsar", key="city_search")
        matches = search_city(query) if query.strip() else []

        if not matches:
            st.warning("No cities found. Try another spelling.")
            st.stop()

        # Several places share a name - there is an Amritsar in more than
        # one country. Show the country so the user can tell them apart.
        options = {
            f"{place['name']}, {place.get('country', '?')}": place for place in matches
        }
        chosen = st.selectbox("Matches", list(options.keys()), key="match_select")
        place = options[chosen]
        latitude, longitude = place["latitude"], place["longitude"]
        label = chosen

    st.caption(f"{latitude}, {longitude}")

weather_data = get_weather(latitude, longitude)

if not (weather_data and "current" in weather_data):
    st.warning("No weather data to show. See the error above.")
    st.stop()

# --- Current conditions (the file 10 dashboard) -------------------------
st.subheader(f"Now in {label}")
current = weather_data["current"]
col1, col2, col3 = st.columns(3)
col1.metric("Temperature", f"{current['temperature_2m']} C")
col2.metric("Wind Speed", f"{current['wind_speed_10m']} km/h")
col3.metric("Humidity", f"{current['relative_humidity_2m']}%")
st.caption(f"Reading taken at {current['time']} ({weather_data['timezone']})")

# === EXTENSION 3 === the hourly chart ===================================
st.subheader("Next 24 hours")
# Day 7's st.line_chart, except the DataFrame came from an API instead of
# a CSV. Nothing about the charting changed - only where the data is from.
st.line_chart(hourly_next_24(weather_data), y="temperature_2m", color="#FF6B5B")

# === EXTENSION 1 === the 7-day forecast =================================
st.subheader("7-day forecast")
forecast = daily_table(weather_data)
st.dataframe(forecast, hide_index=True)

# A second chart off the same table: highs and lows together.
st.line_chart(forecast.set_index("Day")[["High (C)", "Low (C)"]])
