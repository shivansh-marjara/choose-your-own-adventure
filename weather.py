"""Fetch weather from the Open-Meteo APIs; no API key is needed."""

import json
from urllib.parse import quote
from urllib.request import urlopen


def _get_json(url: str) -> dict:
    with urlopen(url, timeout=5) as response:
        data = json.loads(response.read().decode("utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Open-Meteo returned an invalid response")
    return data


def geocode(place: str) -> tuple[float, float, str] | None:
    try:
        url = (
            "https://geocoding-api.open-meteo.com/v1/search"
            f"?name={quote(place, safe='')}&count=1"
        )
        results = _get_json(url).get("results") or []
        if not results:
            return None
        result = results[0]
        if not isinstance(result, dict):
            return None
        name = result["name"]
        if not isinstance(name, str):
            return None
        return float(result["latitude"]), float(result["longitude"]), name
    except Exception:
        return None


def current_weather(lat: float, lon: float) -> dict | None:
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&current=temperature_2m,wind_speed_10m,weather_code,is_day"
    )
    try:
        current = _get_json(url).get("current")
        return current if isinstance(current, dict) else None
    except Exception:
        return None


def describe(weather: dict) -> tuple[str, str]:
    if not isinstance(weather, dict):
        return "grey", "A low grey sky. Nothing moves, and nothing is still."

    weather_code = weather.get("weather_code")
    wind_speed = weather.get("wind_speed_10m")

    try:
        windy = float(wind_speed) >= 35
    except (TypeError, ValueError):
        windy = False

    storm_codes = (
        set(range(51, 68))
        | set(range(80, 83))
        | set(range(95, 100))
    )
    if windy or (isinstance(weather_code, int) and weather_code in storm_codes):
        return "storm", "The sea is running high out there tonight."
    if weather_code == 0:
        return "calm", "Clear sky. The water is a sheet of black glass."
    return "grey", "A low grey sky. Nothing moves, and nothing is still."


def sky_for(place: str) -> dict:
    fallback = {"mood": "calm", "line": None, "place": place, "raw": None}
    try:
        location = geocode(place)
        if location is None:
            return fallback

        latitude, longitude, name = location
        weather = current_weather(latitude, longitude)
        if weather is None:
            return fallback

        mood, line = describe(weather)
        return {"mood": mood, "line": line, "place": name, "raw": weather}
    except Exception:
        return fallback


if __name__ == "__main__":
    print(sky_for("London"))
