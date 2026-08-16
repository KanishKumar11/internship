"""
07_free_apis_demo.py - All five free APIs, working, in one file

TEACHES : Run this to see every free API from the Day 12 slide return
          real data - and to see that the same four-line pattern reads
          five completely different response shapes.
SLIDE   : Day 12, Slide 10 - Reference, Free APIs (deck page 10/16)
RUN     : python 07_free_apis_demo.py

EXPECTED OUTPUT IN THE TERMINAL
        1. OPEN-METEO - weather
           Amritsar: 26.4 C, wind 7.0 km/h
        2. EXCHANGERATE-API - currency
           1 USD = 95.503481 INR  (updated Sun, 16 Aug 2026 ...)
        3. JSONPLACEHOLDER - fake data for testing
           Post 1: "sunt aut facere repellat provident occaecati..."
        4. GITHUB API - repo data
           torvalds has 12 public repos; first 5 listed with star counts
        5. QUOTES - a random quote
           "Life Well Spent Is Long." - Leonardo Da Vinci
        5/5 APIs responded.
    Only the JSONPlaceholder line is fixed - the weather, the rate, the
    repo count and the quote are all live and will differ every run.

REQUIRES
    pip install requests, plus an internet connection.

ONE SUBSTITUTION FROM THE SLIDE
    Slide 10 lists Quotable (api.quotable.io) as the quotes API. Its
    HTTPS certificate has expired, so every call now fails with:
        SSLError: certificate verify failed: certificate has expired
    This file uses dummyjson.com/quotes/random instead - also free, also
    no key, and the response has the same shape (a quote and an author).
    Worth showing the class: APIs die, and error handling is what keeps
    your app standing when they do.
"""

import requests

# One shared helper, because all five calls need the same three
# protections and there is no reason to write them five times.
def fetch_json(label: str, url: str, params: dict | None = None) -> dict | list | None:
    """Call any API safely. Returns parsed JSON, or None if it failed."""
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print(f"   {label}: request timed out.")
    except requests.exceptions.ConnectionError:
        print(f"   {label}: could not connect.")
    except requests.exceptions.HTTPError as error:
        print(f"   {label}: API error {error.response.status_code}.")
    except Exception as error:
        print(f"   {label}: {error}")
    return None


def show_weather() -> bool:
    """Open-Meteo - weather for any lat/lon. No key."""
    print("1. OPEN-METEO - weather")
    data = fetch_json(
        "Open-Meteo",
        "https://api.open-meteo.com/v1/forecast",
        {"latitude": 31.63, "longitude": 74.87, "current": "temperature_2m,wind_speed_10m"},
    )
    if not data:
        return False
    current = data["current"]
    print(f"   Amritsar: {current['temperature_2m']} C, wind {current['wind_speed_10m']} km/h")
    return True


def show_exchange_rate() -> bool:
    """ExchangeRate-API - live currency rates. No key on the open endpoint."""
    print("2. EXCHANGERATE-API - currency")
    data = fetch_json("ExchangeRate", "https://open.er-api.com/v6/latest/USD")
    if not data:
        return False
    # The rates arrive as one big dict of currency code -> number, so you
    # pick the one you want rather than making a call per currency.
    rupees = data["rates"]["INR"]
    print(f"   1 USD = {rupees} INR  (updated {data['time_last_update_utc']})")
    return True


def show_test_post() -> bool:
    """JSONPlaceholder - fake data, for practising against nothing real."""
    print("3. JSONPLACEHOLDER - fake data for testing")
    data = fetch_json("JSONPlaceholder", "https://jsonplaceholder.typicode.com/posts/1")
    if not data:
        return False
    # Useful while you are still learning: you cannot break it, it never
    # rate-limits you, and it always returns the same predictable shape.
    print(f"   Post {data['id']}: \"{data['title'][:60]}...\"")
    return True


def show_github_repos() -> bool:
    """GitHub API - public repo data. No key, but only 60 calls an hour."""
    print("4. GITHUB API - repo data")
    data = fetch_json("GitHub", "https://api.github.com/users/torvalds/repos")
    if not data:
        return False
    # THIS ONE RETURNS A LIST, not a dict. Every other API here hands back
    # an object; this hands back an array, so you index it rather than
    # looking up keys. Always check which you have before navigating.
    print(f"   torvalds has {len(data)} public repos; first 5:")
    for repo in data[:5]:
        stars = repo["stargazers_count"]
        print(f"     {repo['name']:<24} {stars:>7,} stars")
    return True


def show_quote() -> bool:
    """A random quote. See the substitution note in the docstring."""
    print("5. QUOTES - a random quote")
    data = fetch_json("Quotes", "https://dummyjson.com/quotes/random")
    if not data:
        return False
    print(f"   \"{data['quote']}\" - {data['author']}")
    return True


results = [
    show_weather(),
    show_exchange_rate(),
    show_test_post(),
    show_github_repos(),
    show_quote(),
]

print(f"\n{sum(results)}/{len(results)} APIs responded.")

# WHAT THE FIVE HAVE IN COMMON: nothing except the four-line pattern.
# Different URLs, different params, different response shapes - one
# returns a list, the rest return dicts, and every one nests its data
# differently. That is why file 08's four questions matter more than
# memorising any single endpoint.
