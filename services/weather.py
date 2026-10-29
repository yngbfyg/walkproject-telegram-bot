"""Модуль для получения текущей погоды через WeatherAPI.com."""
import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()

# Ключ API WeatherAPI.com
API_KEY: str = os.getenv("WEATHERAPI_KEY", "")


def get_current_weather(lat: float, lon: float) -> Dict[str, Any]:
    """
    Получает текущие метеоданные для заданных координат.

    Выполняет запрос к WeatherAPI.com и возвращает словарь с параметрами:
    температура (°C), описание условий, скорость ветра (км/ч) и влажность (%).

    :param lat: Широта точки.
    :param lon: Долгота точки.
    :return: Словарь с ключами 'temp_c', 'condition', 'wind_kph', 'humidity'.
    """
    url = "https://api.weatherapi.com/v1/current.json"
    params = {
        "key": API_KEY,
        "q": f"{lat},{lon}",
        "lang": "ru"
    }
    resp = requests.get(url, params=params, timeout=5)
    resp.raise_for_status()
    data = resp.json()
    current = data["current"]
    return {
        "temp_c": current["temp_c"],
        "condition": current["condition"]["text"],
        "wind_kph": current["wind_kph"],
        "humidity": current["humidity"],
    }
