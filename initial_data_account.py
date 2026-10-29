"""Модуль для инициализауии датабейза."""
from data.parser import pars_data


def initial_places():
    """Обертка для возвращения изначальных мест."""
    return pars_data()
