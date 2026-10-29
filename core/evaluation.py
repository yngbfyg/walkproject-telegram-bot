"""Модуль оценки и последовательного применения фильтров к списку мест."""

from typing import List, Tuple

from core.models import PlaceDTO

# константы
w_filter_time_to_place: float = 0.33
w_filter_budget: float = 0.5


def init_filter_places(places: List[PlaceDTO]) -> List[int]:
    """
    Инициализирует список индексов мест.

    :param places: Список объектов PlaceDTO
    :return: Список индексов мест
    """
    return list(range(len(places)))


def filter_places_by_tags(
    places: List[PlaceDTO], user_tags: List[str], filter_places: List[int]
) -> List[int]:
    """
    Фильтрует места по пользовательским тегам.

    Оставляет только те индексы из filter_places,
    для которых хотя бы один тег из user_tags присутствует в place.tags.

    :param places: Список объектов PlaceDTO
    :param user_tags: Список тегов, заданных пользователем
    :param filter_places: Текущий список индексов для фильтрации
    :return: Новый список индексов, удовлетворяющих условию
    """
    return [
        i
        for i in filter_places
        if any(tag in places[i].tags for tag in user_tags)
    ]


def filter_places_by_weather(
    places: List[PlaceDTO], weather: str, filter_places: List[int]
) -> List[int]:
    """
    Фильтрует места по погодным условиям.

    Если weather == "indoor", удаляет все места,
    у которых place.weather == "outdoor".
    Иначе возвращает неизменённый список.

    :param places: Список объектов PlaceDTO
    :param weather: Текущие погодные условия
    :param filter_places: Текущий список индексов для фильтрации
    :return: Новый список индексов, удовлетворяющих условию
    """
    if weather == "indoor":
        return [i for i in filter_places if places[i].weather != "outdoor"]
    return filter_places


def filter_places_by_dist(
    available_time: float,
    time_matrix: List[List[Tuple[float, int]]],
    filter_places: List[int],
) -> List[int]:
    """
    Фильтрует места по времени в пути.

    Оставляет индексы i, для которых время пути от стартовой точки
    (time_matrix[0][i+1][0]) не превышает
    w_filter_time_to_place * available_time.

    :param available_time: Доступное время на перемещения
    :param time_matrix: Матрица времени в пути между точками
    :param filter_places: Текущий список индексов для фильтрации
    :return: Новый список индексов, удовлетворяющих условию
    """
    return [
        i
        for i in filter_places
        if time_matrix[0][i + 1][0] <= w_filter_time_to_place * available_time
    ]


def filter_places_by_budget(
    places: List[PlaceDTO], available_budget: float, filter_places: List[int]
) -> List[int]:
    """
    Фильтрует места по бюджету.

    Оставляет индексы i, для которых цена places[i].price
    не превышает w_filter_budget * available_budget.

    :param places: Список объектов PlaceDTO
    :param available_budget: Доступный бюджет пользователя
    :param filter_places: Текущий список индексов для фильтрации
    :return: Новый список индексов, удовлетворяющих условию
    """
    return [
        i
        for i in filter_places
        if places[i].price <= w_filter_budget * available_budget
    ]


def filter_places(
    places: List[PlaceDTO],
    available_time: float,
    available_budget: float,
    user_tags: List[str],
    weather: str,
    time_matrix: List[List[Tuple[float, int]]],
) -> List[int]:
    """
    Применяет последовательность фильтров к списку мест.

    1. По тегам (user_tags)
    2. По погодным условиям (weather)
    3. По времени в пути (available_time)
    4. По бюджету (available_budget)

    :param places: Список объектов PlaceDTO
    :param available_time: Доступное время на весь маршрут
    :param available_budget: Доступный бюджет пользователя
    :param user_tags: Список тегов, заданных пользователем
    :param weather: Текущие погодные условия
    :param time_matrix: Матрица времени в пути между точками
    :return: Список индексов мест, прошедших все фильтры
    """
    indexes = init_filter_places(places)
    indexes = filter_places_by_tags(places, user_tags, indexes)
    indexes = filter_places_by_weather(places, weather, indexes)
    indexes = filter_places_by_dist(available_time, time_matrix, indexes)
    indexes = filter_places_by_budget(places, available_budget, indexes)
    return [i + 1 for i in indexes]


def filter_places_without_tags(
    places: List[PlaceDTO],
    available_time: float,
    available_budget: float,
    weather: str,
    time_matrix: List[List[Tuple[float, int]]],
) -> List[int]:
    """
    Применяет фильтры к списку мест без учёта тегов.

    1. По погодным условиям (weather)
    2. По времени в пути (available_time)
    3. По бюджету (available_budget)

    :param places: Список объектов PlaceDTO
    :param available_time: Доступное время на весь маршрут
    :param available_budget: Доступный бюджет пользователя
    :param weather: Текущие погодные условия
    :param time_matrix: Матрица времени в пути между точками
    :return: Список индексов мест, прошедших все фильтры
    """
    indexes = init_filter_places(places)
    indexes = filter_places_by_weather(places, weather, indexes)
    indexes = filter_places_by_dist(available_time, time_matrix, indexes)
    indexes = filter_places_by_budget(places, available_budget, indexes)
    return [i + 1 for i in indexes]
