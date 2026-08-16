"""
06_streamlit_caching.py - Why every API call in Streamlit gets cached

TEACHES : Day 4's run-loop meeting the internet. Streamlit re-runs the
          whole script on every widget interaction, so an uncached API
          call fires on every keystroke and click. @st.cache_data fixes
          it in one line.
SLIDE   : Day 12, Slide 9 - Pattern, APIs in Streamlit (deck page 09/16)
RUN     : streamlit run 06_streamlit_caching.py

EXPECTED OUTPUT IN THE BROWSER
    A city dropdown, a temperature metric, and a call counter showing how
    many times the API has actually been hit this session.
    Move the slider or retype in the text box: the counter does NOT move,
    because the cached function is not re-entered. Switch city: it goes
    up by one, because the arguments changed. Switch back: it does not
    move again - that result is already cached.

REQUIRES
    pip install requests streamlit
    An internet connection.
"""

import requests
import streamlit as st

URL = "https://api.open-meteo.com/v1/forecast"

CITIES: dict[str, tuple[float, float]] = {
    "Amritsar": (31.63, 74.87),
    "Delhi": (28.61, 77.21),
    "Mumbai": (19.08, 72.88),
}

st.title("Live Weather - with caching")

# A counter that survives reruns, so the class can SEE the difference.
# session_state is Day 5; the API call itself never touches it, which
# matters - see the note about purity at the bottom of this file.
if "api_calls" not in st.session_state:
    st.session_state["api_calls"] = 0


# --- THE FIX: one decorator --------------------------------------------
# ttl=600 means "keep this answer for 600 seconds". Streamlit remembers
# the return value per set of ARGUMENTS: get_weather(31.63, 74.87) and
# get_weather(28.61, 77.21) are cached separately.
@st.cache_data(ttl=600)
def get_weather(latitude: float, longitude: float) -> dict:
    """Fetch current weather. Only actually runs on a cache miss."""
    # This line only executes when the cache does NOT have these
    # arguments. Watch the counter in the UI to see when that happens.
    st.session_state["api_calls"] += 1

    try:
        response = requests.get(
            URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,wind_speed_10m,relative_humidity_2m",
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
    # An empty dict, never None - so the caller can write `if data` and
    # `data.get(...)` without a type check first.
    return {}


# --- WITHOUT CACHING, FOR COMPARISON ------------------------------------
# Delete the decorator above and this is what you get:
#
#   def get_weather(latitude, longitude):
#       response = requests.get(...)      # runs on EVERY rerun
#       return response.json()
#
# Type one letter in a text box -> rerun -> API call.
# Drag a slider ten pixels -> ten reruns -> ten API calls.
# Open-Meteo allows 10,000 calls a day and you can burn hundreds in a
# minute of fiddling. Some APIs cut you off at 60 an hour (GitHub does).

city = st.selectbox("Choose a city", list(CITIES.keys()), key="city_select")
latitude, longitude = CITIES[city]

weather_data = get_weather(latitude, longitude)

# A 200 with an empty body is possible (see file 05), so check the data is
# actually there rather than trusting that the call came back.
if weather_data and "current" in weather_data:
    current = weather_data["current"]
    left, right = st.columns(2)
    left.metric("Temperature", f"{current['temperature_2m']} C")
    right.metric("Wind Speed", f"{current['wind_speed_10m']} km/h")
else:
    st.warning("No weather data to show.")

st.divider()

# --- The demonstration --------------------------------------------------
st.write(f"**Real API calls this session: {st.session_state['api_calls']}**")
st.caption(
    "Move the slider or type below - the counter stays put, because the "
    "cached function is never entered. Change city and it goes up by one."
)

# Two widgets that do nothing except force a rerun, so the point lands.
st.slider("A slider that does nothing", 0, 100, 50, key="dummy_slider")
st.text_input("A text box that does nothing", key="dummy_text")

# THE FOUR RULES OF st.cache_data
#   1. Cache every API call. There is no reason not to.
#   2. Set a ttl. Weather goes stale in minutes; an exchange rate in
#      hours; a list of a user's GitHub repos in days.
#   3. The arguments are the cache key. Same args = cached. Different
#      args = a fresh call.
#   4. The function should be pure - same input, same output, no side
#      effects. The counter above is deliberately breaking that rule to
#      make the caching visible; do not copy that part into real code.
