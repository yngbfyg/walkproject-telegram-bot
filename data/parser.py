"""Парсер для файла базы данных."""
import ast
import os
import re

from core.models import PlaceDTO


def parse_line(line: str) -> PlaceDTO:
    """Парсит строку из places.txt."""
    # Выделяем строку со списком тегов
    list_start = line.find("[")
    list_end = line.find("]", list_start) + 1
    tags_str = line[list_start:list_end]

    # Выделяем строку со словарём расписания
    dict_start = line.find("{", list_end)
    dict_end = line.rfind("}") + 1
    dict_str = line[dict_start:dict_end]

    # Распарсим префикс: name, lat, lon, category, price
    prefix = line[:list_start].rstrip(", ")
    prefix_parts = prefix.split(", ")
    name = prefix_parts[0]
    lat = float(prefix_parts[1])
    lon = float(prefix_parts[2])
    category = prefix_parts[3]
    price = float(prefix_parts[4])

    # Распарсим среднюю часть: avg_visit_time и weather
    middle = line[list_end:dict_start].strip(", ")
    middle_parts = middle.split(", ", 1)
    avg_visit_time = int(middle_parts[0])
    weather = middle_parts[1]

    # Преобразуем теги в список
    tags = ast.literal_eval(tags_str)

    # Очищаем и парсим словарь расписания
    dict_str_clean = re.sub(r'("\d{1,2}:\d{2}),\s*"', r'\1", "', dict_str)
    work_time_dict = ast.literal_eval(dict_str_clean)

    # Создаём и возвращаем DTO
    return PlaceDTO(
        name=name,
        lat=lat,
        lon=lon,
        category=category,
        price=price,
        tags=tags,
        avg_visit_time=avg_visit_time,
        weather=weather,
        work_time_dict=work_time_dict,
    )


def pars_data() -> list[PlaceDTO]:
    """Парсит данные из places.txt."""
    places: list[PlaceDTO] = []
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "places.txt")

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            places.append(parse_line(line))
    return places
