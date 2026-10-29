"""
Модуль определения типа рекомендуемой погоды для прогулки.

Использует данные текущей погоды и возвращает:
  - "indoor" при холоде, осадках или сильном ветре;
  - "outdoor" в остальных случаях.
"""
from typing import Tuple

from services.weather import get_current_weather


def get_type_weather(start: Tuple[float, float]) -> str:
    """
    Определяет, можно ли гулять на улице или стоит выбрать indoor-активность.

    Логика определения:
      1. Если температура ниже 10°C — indoor.
      2. Если в описании условий есть слова 'дожд' или 'снег' — indoor.
      3. Если скорость ветра ≥ 15 км/ч — indoor.
      4. Иначе — outdoor.

    :param start: Координаты начальной точки (широта, долгота).
    :return: "indoor" или "outdoor".
    """
    weather_dict = get_current_weather(start[0], start[1])
    print(weather_dict["temp_c"])
    if weather_dict["temp_c"] < 10.0:
        return "indoor"
    weather_str = weather_dict["condition"]
    if "дожд" in weather_str or "снег" in weather_str:
        return "indoor"
    if weather_dict["wind_kph"] >= 15:
        return "indoor"
    return "outdoor"
