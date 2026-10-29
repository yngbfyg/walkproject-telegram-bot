"""
Модуль сортировки списка маршрутов на основе совпадения тегов и длины маршрута.

Функция route_sort возвращает индексы маршрутов, отсортированные по:
 1. Количеству совпадающих тегов с user_tags (по возрастанию).
 2. Длине маршрута (по возрастанию) для равного количества тегов.
"""

from functools import cmp_to_key
from typing import Callable, List

from core.models import PlaceDTO


def make_item_comparator(
    user_tags: List[str], route_list: List[List[PlaceDTO]]
) -> Callable[[int, int], int]:
    """
    Создаёт функцию сравнения для сортировки маршрутов.

    Функция сравнения возвращает отрицательное число, если маршрут a
    должен идти раньше b, положительное — если позже.

    Сравнение основано на:
      1. Числе совпадающих тегов с user_tags.
      2. При равном числе тегов — длине маршрута.

    :param user_tags: Список тегов, заданных пользователем.
    :param route_list: Список маршрутов, каждый маршрут — список PlaceDTO.
    :return: Функция cmp(a: int, b: int) -> int.
    """

    def cmp(a: int, b: int) -> int:
        """
        Сравнивает два маршрута по индексам a и b.

        :param a: Индекс первого маршрута в route_list.
        :param b: Индекс второго маршрута в route_list.
        :return: Разница по совпадениям тегов или по длине маршрута.
        """
        a_tags = []
        b_tags = []

        for place in route_list[a]:
            a_tags.extend(place.tags)

        for place in route_list[b]:
            b_tags.extend(place.tags)

        a_matches = len(set(user_tags) & set(a_tags))
        b_matches = len(set(user_tags) & set(b_tags))

        if a_matches != b_matches:
            return a_matches - b_matches
        return len(route_list[a]) - len(route_list[b])

    return cmp


def route_sort(
    route_list: List[List[PlaceDTO]], user_tags: List[str]
) -> List[int]:
    """
    Сортирует маршруты и возвращает список их индексов.

    Маршруты сортируются с помощью компаратора, созданого make_item_comparator:
      - По возрастанию числа совпадающих тегов с user_tags.
      - При равных совпадениях — по возрастанию длины маршрута.

    :param route_list: Список маршрутов (каждый маршрут — список PlaceDTO).
    :param user_tags: Список тегов пользователя для сравнения.
    :return: Список индексов маршрутов в отсортированном порядке.
    """
    comparator = make_item_comparator(user_tags, route_list)
    key_func = cmp_to_key(comparator)
    sorted_indices = sorted(range(len(route_list)), key=key_func)
    return sorted_indices
