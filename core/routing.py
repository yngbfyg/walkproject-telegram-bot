"""Модуль генерации маршрута прогулки и расчёта времени и бюджета маршрута."""

import random
from typing import List, Tuple

from core.evaluation import filter_places, filter_places_without_tags
# from data.data_places import PlaceDTO, places
from core.models import PlaceDTO
from utils.time_conv import minutes_since_midnight


def one_walk_budget(
    time_matrix: List[List[Tuple[float, int]]], first: int, second: int
) -> float:
    """
    Рассчитывает стоимость поездки между двумя точками маршрута.

    :param time_matrix: Матрица, содержащая пары
    (время, тип поездки) между точками
    :param first: Индекс начальной точки
    :param second: Индекс конечной точки
    :return: Стоимость поездки, или 0, если тип поездки != 1
    """
    w_one_minute_ride = 8
    if time_matrix[first][second][1] == 1:
        return time_matrix[first][second][0] * w_one_minute_ride
    return 0


def route_budget(
    route: List[int],
    places: List[PlaceDTO],
    time_matrix: List[List[Tuple[float, int]]],
) -> float:
    """
    Вычисляет общий бюджет маршрута и разбивку по перемещениям и посещениям.

    :param route: Список индексов мест маршрута
    :param places: Список объектов PlaceDTO
    :param time_matrix: Матрица (время, тип) между точками маршрута
    :return: Кортеж (общий бюджет, бюджет поездок, бюджет посещений)
    """
    if not route:
        return 0

    moving_budget = []
    places_budget = []
    walk_money = 0

    budget_diff = one_walk_budget(time_matrix, 0, route[0])
    walk_money += budget_diff
    moving_budget.append(budget_diff)

    for i in range(len(route) - 1):
        budget_diff = places[route[i] - 1].price
        walk_money += budget_diff
        places_budget.append(budget_diff)
        budget_diff = one_walk_budget(time_matrix, route[i], route[i + 1])
        walk_money += budget_diff
        moving_budget.append(budget_diff)

    budget_diff = places[route[len(route) - 1] - 1].price
    walk_money += budget_diff
    places_budget.append(budget_diff)
    budget_diff = one_walk_budget(time_matrix, route[len(route) - 1], 0)
    walk_money += budget_diff
    moving_budget.append(budget_diff)
    return (walk_money, moving_budget, places_budget)


def route_time(
    route: List[int],
    places: List[PlaceDTO],
    time_matrix: List[List[Tuple[float, int]]],
) -> float:
    """
    Вычисляет общее время маршрута и разбивку по перемещениям и посещениям.

    :param route: Список индексов мест маршрута
    :param places: Список объектов PlaceDTO
    :param time_matrix: Матрица (время, тип) между точками маршрута
    :return: Кортеж (общее время, список (время, тип) поездок,
    список времени посещений)
    """
    if not route:
        return 0

    moving_time = []
    places_time = []
    walk_time = 0

    diff_time = time_matrix[0][route[0]]
    walk_time += diff_time[0]
    moving_time.append(diff_time)
    for i in range(len(route) - 1):
        diff_time = places[route[i] - 1].avg_visit_time
        walk_time += diff_time
        places_time.append(diff_time)
        diff_time = time_matrix[route[i]][route[i + 1]]
        walk_time += diff_time[0]
        moving_time.append(diff_time)

    diff_time = places[route[len(route) - 1] - 1].avg_visit_time
    walk_time += diff_time
    places_time.append(diff_time)
    diff_time = time_matrix[route[len(route) - 1]][0]
    walk_time += diff_time[0]
    moving_time.append(diff_time)
    return (walk_time, moving_time, places_time)


def generate_route(
    places: List[PlaceDTO],
    current_time: float,
    weather: str,
    current_day: str,
    available_budget: float,
    available_time: float,
    user_tags: List[str],
    time_matrix: List[List[Tuple[float, int]]],
) -> Tuple[List[PlaceDTO], float, float]:
    """
    Генерирует маршрут прогулки с учётом времени, бюджета, тегов и погоды.

    1. Применяет фильтры для отбора доступных мест.
    2. Строит словари кандидатов 'с тегами' и 'без тегов'.
    3. Последовательно выбирает следующие точки,
    проверяя рабочее время и ограничения.

    :param places: Все возможные места для маршрута
    :param start: Координаты начальной точки (широта, долгота)
    :param current_time: Текущее время в минутах от полуночи
    :param weather: Текущие погодные условия
    :param current_day: День недели для проверки work_time_dict
    :param available_budget: Доступный бюджет пользователя
    :param available_time: Доступное время пользователя в минутах
    :param user_tags: Список предпочитаемых тегов
    :param time_matrix: Матрица времени и типов поездок
    :return: Кортеж (список мест маршрута, результат route_time,
    результат route_budget)
    """
    indexes_filter_places = filter_places(
        places,
        available_time,
        available_budget,
        user_tags,
        weather,
        time_matrix,
    )
    indexes_filter_places_without_tags = filter_places_without_tags(
        places, available_time, available_budget, weather, time_matrix
    )

    top_places = 5  # количество мест из которых мы будем выбирать следующее

    # словари, в которых будут хранится кандидаты на следующую точку
    top_without_tags = (
        {}
    )  # словарь, в котором хранятся места без тегов
    topk = (
        {}
    )  # словарь, в котором хранятся топ k мест

    for current_place_ind in range(len(places) + 1):
        # создаем списки
        topk[current_place_ind] = []
        top_without_tags[current_place_ind] = []

        # кладем все подходящие элменты в словари
        for next_place_ind in range(1, len(places) + 1):
            if current_place_ind == next_place_ind:
                continue

            if next_place_ind in indexes_filter_places:
                topk[current_place_ind].append(next_place_ind)

            if next_place_ind in indexes_filter_places_without_tags:
                top_without_tags[current_place_ind].append(next_place_ind)

        # сортируем по времени, которым можно добраться
        top_without_tags[current_place_ind] = sorted(
            top_without_tags[current_place_ind],
            key=lambda j: time_matrix[current_place_ind][j],
        )
        topk[current_place_ind] = sorted(
            topk[current_place_ind],
            key=lambda j: time_matrix[current_place_ind][j],
        )

        # оставляем первые k элементов в topk
        topk[current_place_ind] = topk[current_place_ind][:top_places]

    result_route = []  # массив индексов мест из нашего маршрута

    money_spent = 0  # постраченные деньги за время маршрута
    time_spent = 0  # потраченное время на маршрут

    last_walk_money_spent = (
        0  # деньги, потраченные на возвращение в начальную точку
    )
    last_walk_time_spent = (
        0  # время, потраченное на возвращение в начальную точку
    )

    current_place_ind = 0  # индекс места, в котором мы сейчас

    cnt_without_food = 2  # количество мест, в которых мы не ели
    cnt_without_drink = 2  # количество мест, в которых мы не пили

    while (
        money_spent + last_walk_money_spent <= available_budget
        and time_spent + last_walk_time_spent <= available_time
    ):

        # обновляем счетчики
        cnt_without_food += 1
        cnt_without_drink += 1

        if (
            current_place_ind != 0
            and "food" in places[current_place_ind - 1].tags
        ):
            cnt_without_food = 0

        if (
            current_place_ind != 0
            and "drink" in places[current_place_ind - 1].tags
        ):
            cnt_without_drink = 0

        # создаем кандидатов
        candidates_with_tags = topk[current_place_ind].copy()
        candidates_without_tags = top_without_tags[current_place_ind].copy()

        # фильтруем кандидатов, если мы уже ели/пили недавно
        if cnt_without_food <= 2:
            candidates_with_tags = [
                i
                for i in candidates_with_tags
                if "food" not in places[i - 1].tags
            ]
            candidates_without_tags = [
                i
                for i in candidates_without_tags
                if "food" not in places[i - 1].tags
            ]

        if cnt_without_drink <= 1:
            candidates_with_tags = [
                i
                for i in candidates_with_tags
                if "drink" not in places[i - 1].tags
            ]
            candidates_without_tags = [
                i
                for i in candidates_without_tags
                if "drink" not in places[i - 1].tags
            ]

        is_taken = 0  # 1 - мы взяли место, иначе - 0
        next_place_ind = 0  # следующий индекс, который мы выбираем

        # попытаемся взять из кандидатов с тегами
        while candidates_with_tags:
            next_place_ind = random.choice(candidates_with_tags)
            # проверка по рабочему времени
            open_time, close_time = places[next_place_ind - 1].work_time_dict[
                current_day
            ]
            time_add = (
                places[next_place_ind - 1].avg_visit_time
                + time_matrix[current_place_ind][next_place_ind][0]
                + time_matrix[next_place_ind][0][0]
            )
            if (
                current_time + places[next_place_ind - 1].avg_visit_time
                <= minutes_since_midnight(close_time)
                and current_time >= minutes_since_midnight(open_time)
                and time_add + time_spent <= available_time
            ):
                is_taken = 1
                break
            candidates_with_tags.remove(next_place_ind)

        if is_taken == 0:
            # попытаемся взять из кандидатов без тегов
            while candidates_without_tags:
                next_place_ind = random.choice(candidates_without_tags)
                # проверка по рабочему времени
                open_time, close_time = places[
                    next_place_ind - 1
                ].work_time_dict[current_day]
                time_add = (
                    places[next_place_ind - 1].avg_visit_time
                    + time_matrix[current_place_ind][next_place_ind][0]
                    + time_matrix[next_place_ind][0][0]
                )
                if (
                    current_time + places[next_place_ind - 1].avg_visit_time
                    <= minutes_since_midnight(close_time)
                    and current_time >= minutes_since_midnight(open_time)
                    and time_add + time_spent <= available_time
                ):
                    is_taken = 1
                    break
                candidates_without_tags.remove(next_place_ind)

        if is_taken == 0:
            break

        # удалим место из всех кандидатов, потому что мы в нем побывали
        for current, lst in topk.items():
            # перестроить список без next_ind
            topk[current] = [i for i in lst if i != next_place_ind]

        for current, lst in top_without_tags.items():
            top_without_tags[current] = [i for i in lst if i != next_place_ind]

        # обновим все переменные
        money_spent += places[next_place_ind - 1].price
        money_spent += one_walk_budget(
            time_matrix, current_place_ind, next_place_ind
        )
        last_walk_money_spent = one_walk_budget(time_matrix, next_place_ind, 0)

        time_spent += places[next_place_ind - 1].avg_visit_time
        time_spent += time_matrix[current_place_ind][next_place_ind][0]
        last_walk_time_spent = time_matrix[next_place_ind][0][0]

        result_route.append(next_place_ind)
        current_place_ind = next_place_ind

    # удалим последний элемент, если сработало условие while
    if (
        money_spent + last_walk_money_spent > available_budget
        or time_spent + last_walk_time_spent > available_time
    ):

        if len(result_route) > 0:
            result_route.pop()

    result = []
    # print(result_route)
    for i in result_route:
        result.append(places[i - 1])
    # print(route_time(result_route, places, start, time_matrix))
    # print(route_budget(result_route, places, start, time_matrix))
    result_time = route_time(result_route, places, time_matrix)
    result_budget = route_budget(result_route, places, time_matrix)
    return (result, result_time, result_budget)
