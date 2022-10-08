import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(planetname):

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://api.le-systeme-solaire.net/rest/bodies/{urllib.parse.quote_plus(planetname)}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        data = response.json()
        return {
            "mass": data["mass"],
            "vol": data["vol"],
            "density": data["density"],
            "gravity": data["gravity"],
            "avgTemp": data["avgTemp"],
            "moons": data["moons"],
            "englishName": data["englishName"]
        }
    except (KeyError, TypeError, ValueError):
        return None

def lookupmoon(url):

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        data = response.json()
        return {
            "mass": data["mass"],
            "semimajorAxis": data["semimajorAxis"],
            "meanRadius": data["meanRadius"],
            "sideralOrbit": data["sideralOrbit"],
            "discoveredBy": data["discoveredBy"],
            "discoveryDate": data["discoveryDate"],
            "englishName": data["englishName"]
        }
    except (KeyError, TypeError, ValueError):
        return None

def rover(name, sol):

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{urllib.parse.quote_plus(name)}/photos?sol={urllib.parse.quote_plus(sol)}&api_key={api_key}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        data = response.json()
        return {
            "all": data["photos"],
        }
    except (KeyError, TypeError, ValueError):
        return None

def marsweather():

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://api.nasa.gov/insight_weather/?api_key={api_key}&feedtype=json&ver=1.0"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        data = response.json()
        for i in data:
            return data[i]["AT"], data[i]["HWS"], data[i]["PRE"], data[i]["WD"]
    except (KeyError, TypeError, ValueError):
        return None
def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

