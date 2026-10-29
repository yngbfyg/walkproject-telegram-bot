"""Модуль-обработчик истории прогулок пользователя."""
from telebot import TeleBot
from telebot.types import Message

from utils_bot.history import user_history


def register_history_handlers(bot: TeleBot) -> None:
    """
    Регистрирует обработчик кнопки '🎞️ история'.

    При нажатии пользователю отправляется список
    ранее сгенерированных маршрутов.
    Если истории нет — уведомляет об отсутствии прогулок.

    :param bot: Экземпляр TeleBot
    """
    @bot.message_handler(func=lambda m: m.text == "🎞️ история")
    def on_history_button(message: Message) -> None:
        """
        Обрабатывает нажатие кнопки '🎞️ история'.

        :param message: Объект сообщения от пользователя
        """
        if (len(user_history[message.chat.id]) == 0):
            bot.send_message(
                message.chat.id,
                'к сожалению, у тебя еще не было прогулок (｡T ω T｡)'
            )
        else:
            msg = ""
            cnt = 1
            for route in user_history[message.chat.id][-10:]:
                msg += (
                    f'<i>{cnt}: '
                    f'{", ".join(str(place) for place in route)}</i>\n'
                )
                cnt += 1
            bot.send_message(
                message.chat.id,
                'вот история твоих прогулок!\n' + msg,
                parse_mode="HTML"
            )
