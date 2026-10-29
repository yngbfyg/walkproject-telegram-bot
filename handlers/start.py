"""
Модуль регистрации стартовых обработчиков Telegram-бота.

Содержит функции для инициализации пользовательских данных.
"""
from telebot import TeleBot
from telebot.types import Message

from keyboards.reply_keyboard import initial_data_keyboard
from utils_bot.history import user_history
from utils_bot.storage import user_data


def start_handler(message: Message, bot: TeleBot) -> None:
    """
    Обрабатывает команду /start и инициализирует сессию пользователя.

    Очищает/создаёт структуры user_data и user_history для данного chat_id,
    отправляет приветственное сообщение с начальной клавиатурой и стикер.

    :param message: Объект входящего сообщения от пользователя.
    :param bot: Экземпляр TeleBot для отправки сообщений.
    """
    user_data[message.chat.id] = {}
    user_history.setdefault(message.chat.id, [])
    bot.send_message(
        message.chat.id,
        "хей! я помогу тебе выбрать маршрут по самым вайбовым местам!! <3\n"
        "но сначала надо учесть все твои пожелания. с чего начнем?",
        reply_markup=initial_data_keyboard(),
    )
    sticker_id = (
        "CAACAgIAAxkBAAEOcqVoH3_j4HS9BmXcGttSpokSKctL8gACfWEAAttEwEof"
        "MQrJFFG_djYE"
    )
    bot.send_sticker(message.chat.id, sticker_id)


def register_start_handlers(bot: TeleBot) -> None:
    """
    Регистрирует обработчик команды /start.

    :param bot: Экземпляр TeleBot для регистрации хендлера.
    """
    bot.register_message_handler(
        lambda msg: start_handler(msg, bot), commands=["start"]
    )
