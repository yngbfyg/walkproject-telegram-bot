"""Модуль работы с GraphHopper API для расчёта времени маршрута."""

import os
import time
from typing import List, Tuple

import requests
from dotenv import load_dotenv

from core.models import PlaceDTO

load_dotenv()

# Читаем API-ключ из окружения
API_KEY: str = os.getenv("TRAVEL_TIME_API_KEY", "")

# Максимум пешей прогулки в минутах
max_walk_time: float = 25.0


def safe_get(url: str, **kwargs) -> requests.Response:
    """
    Выполняет GET-запрос с экспоненциальным бэкоффом при ответе 429.

    :param url: URL для запроса.
    :param kwargs: Дополнительные параметры для requests.get.
    :return: Успешный объект Response.
    :raises HTTPError: если другие ошибки HTTP.
    """
    backoff = 1
    for _ in range(5):
        resp = requests.get(url, **kwargs)
        if resp.status_code == 429:
            wait = int(resp.headers.get("Retry-After", backoff))
            time.sleep(wait)
            backoff *= 2
            continue
        resp.raise_for_status()
        return resp
    resp.raise_for_status()
    return resp


def get_travel_time(
    origin: Tuple[float, float], destination: Tuple[float, float]
) -> Tuple[float, int]:
    """
    Возвращает время поездки между двумя точками и режим поездки.

    Если время пешком превышает max_walk_time, переключается на автомобиль,
    добавляет фиксированный 5-минутный наценки и возвращает флаг 1.
    В противном случае возвращает время ходьбы и флаг 0.

    :param origin: Координаты (широта, долгота) начальной точки.
    :param destination: Координаты (широта, долгота) конечной точки.
    :return: Кортеж (duration_minutes, mode_flag).
             mode_flag = 0 для пешего, 1 для авто.
    :raises RuntimeError: если API_KEY не задан.
    """
    base_url = "https://graphhopper.com/api/1/route"
    params = {
        "point": [
            f"{origin[0]},{origin[1]}",
            f"{destination[0]},{destination[1]}",
        ],
        "vehicle": "foot",
        "points_encoded": "false",
        "key": API_KEY,
    }

    # пешком
    data = safe_get(base_url, params=params).json()
    walk_min = data["paths"][0]["time"] / 1000 / 60

    if walk_min > max_walk_time:
        # если пешком слишком долго — машина
        params["vehicle"] = "car"
        data_car = safe_get(base_url, params=params).json()
        car_min = data_car["paths"][0]["time"] / 1000 / 60
        return (car_min + 5.0, 1)

    return (walk_min, 0)


def get_time_matrix(places: List[PlaceDTO]) -> List[List[Tuple[float, int]]]:
    """
    Строит матрицу N×N пар (time_minutes, mode_flag) для всех мест.

    :param places: Список объектов PlaceDTO.
    :return: Матрица вида [[...], ...],
    где indices 0..N-1 соответствуют places.
    """
    n = len(places)
    # инициализируем матрицу нулями (пешком, 0 минут)
    matrix: List[List[Tuple[float, int]]] = [
        [(0.0, 0) for _ in range(n)] for _ in range(n)
    ]

    for i in range(n):
        for j in range(n):
            if i >= j:
                continue
            print(i, j)
            matrix[i][j] = get_travel_time(
                (places[i].lat, places[i].lon), (places[j].lat, places[j].lon)
            )
            matrix[j][i] = matrix[i][j]
            time.sleep(3)  # чтобы не спамить API
    return matrix


def update_time_matrix(
    matrix: List[List[Tuple[float, int]]],
    places: List[PlaceDTO],
    start: Tuple[float, float],
) -> List[List[Tuple[float, int]]]:
    """
    Добавляет или обновляет нулевой ряд и столбец в матрице.

    Если matrix N×N — возвращает новую (N+1)×(N+1).
    Если уже (N+1)×(N+1) — обновляет in-place.

    :param matrix: Существующая матрица  N×N или (N+1)×(N+1).
    :param places: Список PlaceDTO длины N.
    :param start: Координаты начальной точки.
    :return: Новая или обновлённая матрица.
    :raises ValueError: если размер matrix неожидан.
    """
    n = len(places)

    # пересчитаем кортежи для 0-го ряда (от старта до всех точек)
    first_row: List[Tuple[float, int]] = [(0.0, 0)]
    for p in places:
        first_row.append(get_travel_time(start, (p.lat, p.lon)))
        time.sleep(3)  # чтобы не спамить API

    # если матрица размера N×N — расширяем
    if len(matrix) == n and all(len(row) == n for row in matrix):
        # строим новую матрицу (N+1)×(N+1)
        new_matrix: List[List[Tuple[float, int]]] = [first_row]
        for i, row in enumerate(matrix):
            # в каждой строке добавляем в начало время от старта до places[i]
            new_matrix.append([first_row[i + 1]] + row)
        return new_matrix

    # иначе, если матрица уже (N+1)×(N+1) — обновляем in-place
    if len(matrix) == n + 1 and all(len(row) == n + 1 for row in matrix):
        # обновляем 0-й ряд
        matrix[0] = first_row
        # обновляем 0-й столбец в остальных строках
        for i in range(1, n + 1):
            matrix[i][0] = first_row[i]
        return matrix

    # во всех остальных случаях можно выбросить ошибку
    # или привести к расширению
    raise ValueError(
        f"Неподдерживаемый размер матрицы: {len(matrix)}×{len(matrix[0])}, "
        f"ожидался {n}×{n} или {n+1}×{n+1}"
    )
