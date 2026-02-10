import os
import requests
from typing import Dict, Any
from requests.exceptions import RequestException, Timeout


BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
DEFAULT_TIMEOUT = 10  # in seconds


class WeatherAPIError(Exception):
    """Custom exception for weather API related errors."""
    pass


def get_weather(city: str, api_key: str) -> Dict[str, Any]:
    """
    Fetch current weather data for a given city.

    :param city: Name of the city
    :param api_key: OpenWeatherMap API key
    :return: Dictionary containing weather information
    :raises WeatherAPIError: If API request fails or returns an error
    """
    if not api_key:
        raise WeatherAPIError("API key is missing. Set OPENWEATHER_API_KEY.")

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
    }

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            timeout=DEFAULT_TIMEOUT
        )
        response.raise_for_status()

    except Timeout:
        raise WeatherAPIError("Request timed out. Please try again later.")

    except RequestException as exc:
        raise WeatherAPIError(f"Network error occurred: {exc}")

    data = response.json()

    
    

    
    if data.get("cod") != 200:
        message = data.get("message", "Unknown error")
        raise WeatherAPIError(f"API error: {message}")

    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
    }


def display_weather(weather: Dict[str, Any]) -> None:
    """
    Display weather information in a readable format.
    """
    print(f"\nWeather in {weather['city']}, {weather['country']}")
    print("-" * 35)
    print(f"Temperature : {weather['temperature']}°C")
    print(f"Condition   : {weather['description'].capitalize()}")
    print(f"Humidity    : {weather['humidity']}%")
    print(f"Pressure    : {weather['pressure']} hPa")
    print("-" * 35)


def main() -> None:
    """
    Entry point for the weather application.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    city = input("Enter the city name: ").strip()

    if not city:
        print("City name cannot be empty.")
        return

    try:
        weather = get_weather(city, api_key)
        display_weather(weather)

    except WeatherAPIError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
