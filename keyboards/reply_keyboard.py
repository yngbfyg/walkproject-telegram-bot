"""Взаимодействие с интерфейсом бота."""
from telebot.types import KeyboardButton, ReplyKeyboardMarkup


def initial_data_keyboard() -> ReplyKeyboardMarkup:
    """Создаёт клавиатуру для ввода начальных данных пользователя."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("🤑 бюджет"),
        KeyboardButton("⏱️ время прогулки")
    )
    markup.add(
        KeyboardButton("💌 теги"),
    )
    markup.add(
        KeyboardButton("🎞️ история"),
    )
    return markup


def location_keyboard() -> ReplyKeyboardMarkup:
    """Создаёт клавиатуру для запроса локации пользователя."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("🌎 локация", request_location=True),
    )
    markup.add(
        KeyboardButton("🎞️ история"),
    )
    return markup


def number_3_keyboard() -> ReplyKeyboardMarkup:
    """Создаёт клавиатуру для выбора одного из трёх вариантов."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("1️⃣"),
        KeyboardButton("2️⃣")
    )
    markup.add(
        KeyboardButton("3️⃣"),
    )
    markup.add(
        KeyboardButton("🎞️ история"),
    )
    return markup


def number_2_keyboard() -> ReplyKeyboardMarkup:
    """Создаёт клавиатуру для выбора одного из двух вариантов."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("1️⃣"),
        KeyboardButton("2️⃣")
    )
    markup.add(
        KeyboardButton("🎞️ история"),
    )
    return markup


def history_keyboard() -> ReplyKeyboardMarkup:
    """Создаёт клавиатуру для доступа к истории прогулок."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("🎞️ история"),
    )
    return markup
