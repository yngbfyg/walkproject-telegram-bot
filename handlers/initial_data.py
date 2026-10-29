"""Модуль регистрации хендлеров для ввода."""
from telebot import TeleBot
from telebot.types import Message

from handlers.route import send_route
from keyboards.reply_keyboard import history_keyboard, location_keyboard
from utils_bot.storage import user_data


def register_budget_handlers(bot: TeleBot) -> None:
    """
    Регистрирует обработчики для кнопки '🤑 бюджет'.

    После нажатия кнопки бот запрашивает ввод бюджета и сохраняет его.
    Если введены не все данные (бюджет, время, теги)
    предлагает нажать ещё кнопки.
    После ввода всех трёх параметров предлагает отправить локацию.

    :param bot: Экземпляр TeleBot
    """
    @bot.message_handler(func=lambda m: m.text == "🤑 бюджет")
    def on_budget_button(message: Message) -> None:
        """
        Обрабатывает нажатие кнопки '🤑 бюджет'.

        Запрашивая у пользователя бюджет.

        :param message: Сообщение с текстом кнопки
        """
        msg = bot.send_message(
            message.chat.id, "введи свой бюджет (в рублях!) 🙏🏻🙏🏻"
        )
        bot.register_next_step_handler(msg, process_budget)

    def process_budget(message: Message) -> None:
        """
        Обрабатывает ввод бюджета пользователем и сохраняет его.

        :param message: Сообщение с текстом введённого бюджета.
        """
        try:
            budget = int((message.text or "").strip())
            if budget < 0:
                raise ValueError("Negative budget")
        except ValueError:
            reply = bot.send_message(
                message.chat.id,
                "введи бюджет целым неотрицательным числом (в рублях!) 🙏🏻",
            )
            bot.register_next_step_handler(reply, process_budget)
            return
        user_data.setdefault(message.chat.id, {})
        user_data[message.chat.id]["budget"] = budget
        if len(user_data[message.chat.id]) != 3:
            bot.send_message(
                message.chat.id,
                f"супии! запомнил твой бюджет: {budget}р.\n"
                f"мне нужно еще немного информации, тыкни еще кнопку! 😮‍💨",
            )
        else:
            bot.send_message(
                message.chat.id,
                f"супии! запомнил твой бюджет: {budget}р.\n"
                f"осталось совсем чуть-чуть, пришли "
                "мне свою текущую локацию! 😈",
                reply_markup=location_keyboard(),
            )


def register_walking_time_handlers(bot: TeleBot) -> None:
    """
    Регистрирует обработчики для кнопки '⏱️ время прогулки'.

    Бот запрашивает желаемую длительность прогулки и сохраняет её.
    После ввода всех трёх параметров предлагает отправить локацию.

    :param bot: Экземпляр TeleBot
    """
    @bot.message_handler(func=lambda m: m.text == "⏱️ время прогулки")
    def on_walking_time_button(message: Message) -> None:
        """
        Обрабатывает нажатие кнопки '⏱️ время прогулки'.

        :param message: Сообщение с текстом кнопки.
        """
        msg = bot.send_message(
            message.chat.id,
            "введи желаемое время прогулки (в минутах!) 🙏🏻🙏🏻",
        )
        bot.register_next_step_handler(msg, process_time)

    def process_time(message: Message) -> None:
        """
        Обрабатывает ввод времени прогулки и сохраняет его.

        :param message: Сообщение с текстом введённого времени.
        """
        try:
            time = int((message.text or "").strip())
            if time <= 0:
                raise ValueError("Non-positive walking time")
        except ValueError:
            reply = bot.send_message(
                message.chat.id,
                "введи время прогулки целым положительным числом минут 🙏🏻",
            )
            bot.register_next_step_handler(reply, process_time)
            return
        user_data.setdefault(message.chat.id, {})
        user_data[message.chat.id]["time"] = time
        if len(user_data[message.chat.id]) != 3:
            bot.send_message(
                message.chat.id,
                "супии! запомнил время, которое ты потратишь "
                f"на лучшую прогулку: {time}мин.\n"
                f"мне нужно еще немного информации, тыкни еще кнопку! 😮‍💨",
            )
        else:
            bot.send_message(
                message.chat.id,
                "супии! запомнил время, которое ты"
                f"потратишь на лучшую прогулку: {time}мин.\n"
                "осталось совсем чуть-чуть, пришли"
                f"мне свою текущую локацию! 😈",
                reply_markup=location_keyboard(),
            )


def register_tags_handlers(bot: TeleBot) -> None:
    """
    Регистрирует обработчики для кнопки '💌 теги' и ввода тегов.

    Бот предлагает список тегов и сохраняет выбранные через пробел.
    После ввода всех трёх параметров предлагает отправить локацию.

    :param bot: Экземпляр TeleBot.
    """
    @bot.message_handler(func=lambda m: m.text == "💌 теги")
    def on_tags_button(message: Message) -> None:
        """
        Обрабатывает нажатие кнопки '💌 теги'.

        Предлагая пользователю теги.

        :param message: Сообщение с текстом кнопки.
        """
        msg = bot.send_message(
            message.chat.id,
            "выбери теги, чтобы прогулка "
            "соответствовала всем твоим пожеланиям! 😇\n"
            "напиши понравившиеся из этого списка через пробел! ^_^\n\n"
            "<i>food, drink, park, art, vegan, graffiti, </i>"
            "<i>streetfood, bar, gothic, temple, baroque, burgers </i>"
            "<i>japan, bubble-tea, botanic-garden, vintage, second-hand</i>",
            parse_mode="HTML",
        )
        bot.register_next_step_handler(msg, process_tags)

    def process_tags(message: Message) -> None:
        """
        Обрабатывает ввод тегов и сохраняет их.

        :param message: Сообщение с текстом введённых тегов.
        """
        text = message.text.strip()
        tags = list(text.split())
        user_data.setdefault(message.chat.id, {})
        user_data[message.chat.id]["tags"] = tags
        tags_str = ", ".join(tags)
        if len(user_data[message.chat.id]) != 3:
            bot.send_message(
                message.chat.id,
                f"супии! запомнил твои теги: _{tags_str}_\n"
                f"мне нужно еще немного информации, тыкни еще кнопку! 😮‍💨",
                parse_mode="Markdown",
            )
        else:
            bot.send_message(
                message.chat.id,
                f"супии! запомнил твои теги: _{tags_str}_\n"
                "осталось совсем чуть-чуть, "
                "пришли мне свою текущую локацию! 😈",
                parse_mode="Markdown",
                reply_markup=location_keyboard(),
            )


def register_location_handlers(bot: TeleBot) -> None:
    """
    Регистрирует обработчик для получения локации и запуск генерации.

    Сохраняет координаты пользователя
    и отправляет маршрут и кнопку истории.

    :param bot: Экземпляр TeleBot.
    """
    @bot.message_handler(content_types=["location"])
    def on_location_button(message: Message) -> None:
        """
        Обрабатывает получение локации пользователя.

        :param message: Сообщение с полем location.
        """
        latitude = message.location.latitude
        longitude = message.location.longitude

        user_data.setdefault(message.chat.id, {})
        user_data[message.chat.id]["location"] = {
            "lat": latitude,
            "lon": longitude,
        }
        bot.send_message(
            message.chat.id,
            'супии! получил твою локацию 😈😈\n'
            'это всё, что мне было нужно! сейчас сгнерирую пути, '
            'выбирай понравившийся! ૮₍ ˶• ༝ •˶ ₎ა',
            reply_markup=history_keyboard()
        )
        send_route(bot, message)
