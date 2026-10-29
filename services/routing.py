"""Сервис для расчёта времени маршрутов через GraphHopper API."""
import os
from typing import Tuple

import requests
from dotenv import load_dotenv

load_dotenv()

# API-ключ GraphHopper
GRAPHOPPER_API_KEY: str = os.getenv("GRAPHOPPER_API_KEY")

# Эндпоинты GraphHopper Directions и Matrix API
GRAPHOPPER_ROUTE_URL: str = "https://graphhopper.com/api/1/route"
GRAPHOPPER_MATRIX_URL: str = "https://graphhopper.com/api/1/matrix"


def get_travel_time_graphhopper(
    origin: Tuple[float, float],
    destination: Tuple[float, float],
    vehicle: str = "car"
) -> float:
    """
    Вычисляет время поездки между двумя точками.

    :param origin: Координаты (широта, долгота) начальной точки.
    :param destination: Координаты (широта, долгота) конечной точки.
    :param vehicle: Профиль маршрута — "car", "bike" или "foot".
    :return: Примерное время поездки в минутах.
    """
    params = {
        "point": [
            f"{origin[0]},{origin[1]}",
            f"{destination[0]},{destination[1]}"
        ],
        "vehicle": vehicle,
        "points_encoded": "false",
        "key": GRAPHOPPER_API_KEY
    }
    response = requests.get(GRAPHOPPER_ROUTE_URL, params=params)
    response.raise_for_status()
    data = response.json()
    # 'time' в миллисекундах в первом пути
    time_ms = data.get("paths", [])[0].get("time", 0)
    # Конвертация в минуты
    return time_ms / 60000.0
