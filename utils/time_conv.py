"""Модуль конвертации времени."""


def minutes_since_midnight(time_str: str) -> int:
    """
    Преобразует строку формата "HH:MM" в количество минут с начала суток.

    :param time_str: Время в формате "HH:MM".
    :return: Количество минут, прошедших с 00:00.
    """
    hours_str, minutes_str = time_str.split(":")
    hours = int(hours_str)
    minutes = int(minutes_str)
    return hours * 60 + minutes
