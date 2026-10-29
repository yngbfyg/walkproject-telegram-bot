"""
Модуль обработки и отправки маршрута прогулки пользователю Telegram-бота.

Содержит функцию send_route, которая собирает пользовательские данные,
генерирует несколько вариантов маршрутов с учётом времени, бюджета,
погодных условий и тегов, сортирует их и отправляет пользователю.
"""
from datetime import datetime
from zoneinfo import ZoneInfo

from telebot import TeleBot
from telebot.types import Message

from core.routing import generate_route
from data.kreml_time_matrix import kreml_time_matrix
from keyboards.reply_keyboard import (history_keyboard, number_2_keyboard,
                                      number_3_keyboard)
from utils.route_sort import route_sort
from utils.weather import get_type_weather
from utils.time_conv import minutes_since_midnight
from utils_bot.history import user_history
from utils_bot.storage import user_data


def send_route(bot: TeleBot, message: Message) -> None:
    """
    Генерирует и отправляет пользователю варианты маршрутов прогулки.

    Функция выполняет следующие шаги:
      1. Извлекает из user_data параметры пользователя: местоположение,
         бюджет, доступное время и теги.
      2. Определяет текущие погодные условия и время в Москве.
      3. Генерирует несколько маршрутов с помощью generate_route.
      4. Фильтрует уникальные маршруты, сортирует их и выбирает топ 2 или 3.
      5. Отправляет пользователю клавиатуру для выбора варианта.
      6. По выбору пользователя отправляет детальный маршрут и
         сохраняет историю в user_history.

    :param bot: Экземпляр TeleBot.
    :param message: Сообщение от пользователя с локацией и параметрами.
    """
    start = (
        user_data[message.chat.id]["location"]["lat"],
        user_data[message.chat.id]["location"]["lon"],
    )
    # A fixed Kremlin-based matrix avoids expensive per-user GraphHopper
    # recomputation on the free API tier. Location is still used for weather.
    time_matrix_new = kreml_time_matrix
    weather = get_type_weather(start)
    moscow_tz = ZoneInfo("Europe/Moscow")
    now = datetime.now(moscow_tz)
    #current_time = 12 * 60
    current_time = minutes_since_midnight(now.strftime('%H:%M'))
    weekday = now.strftime("%a").lower()
    available_budget = float(user_data[message.chat.id]["budget"])
    walking_time = float(user_data[message.chat.id]["time"])
    tags = user_data[message.chat.id]["tags"]
    print(weather, weekday, current_time, available_budget, walking_time, tags)
    all_routes = []
    final_places = []
    budgets = []
    times = []
    for i in range(15):
        route = generate_route(
            bot.places,
            current_time,
            weather,
            weekday,
            available_budget,
            walking_time,
            tags,
            time_matrix_new,
        )
        if not route[0]:
            continue
        if route[0] not in all_routes:
            places = route[0]
            time = route[1]
            budget = route[2]
            final_places.append(places)
            names = []
            for place in places:
                names.append(place.name)
            budgets.append(budget)
            times.append(time)
            all_routes.append(places)

    if len(final_places) < 2:
        bot.send_message(
            message.chat.id,
            'похоже с этими параметрами не получилось '
            'подобрать несколько вариантов прогулки 😞\n'
            'попробуй еще раз, нажав /start 💘',
            reply_markup=history_keyboard()
        )
        return

    final_cnt = min(3, len(final_places))
    sorted_ind = route_sort(final_places, tags)[::-1][:final_cnt]
    sorted_names = []
    sorted_times = []
    sorted_budgets = []

    for ind in sorted_ind:
        places = final_places[ind]
        names = []
        for place in places:
            names.append(place.name)
        sorted_names.append(names)
        sorted_times.append(times[ind])
        sorted_budgets.append(budgets[ind])

    '''for ind in range(final_cnt):
        print(sorted_names[ind])
        print(sorted_times[ind])
        print(sorted_budgets[ind])'''

    messages = []
    for i in range(final_cnt):
        msg = ""
        times_res = sorted_times[i]
        budgets_res = sorted_budgets[i]
        names_res = sorted_names[i]
        cnt = 1
        msg += f"1: центр Москвы (условная стартовая точка) -> {names_res[0]}\n"
        cnt += 1
        if times_res[1][0][1] == 1:
            msg += "🚗  "
        else:
            msg += "🚶  "
        msg += (
            f"в дороге: {int(times_res[1][0][0])}мин.  "
            f"({int(budgets_res[1][0])}р.)\n"
        )
        msg += (
            f"⏱️  на месте: {int(times_res[2][0])}мин.  "
            f"({int(budgets_res[2][0])}р.)\n\n"
        )
        for j in range(len(names_res) - 1):
            msg += f"{cnt}: {names_res[j]} -> {names_res[j+1]}\n"
            cnt += 1
            if times_res[1][j + 1][1] == 1:
                msg += "🚗  "
            else:
                msg += "🚶  "
            msg += (
                f"в дороге: {int(times_res[1][j+1][0])}мин.  "
                f"({int(budgets_res[1][j+1])}р.)\n"
            )
            msg += (
                f"⏱️  на месте: {int(times_res[2][j+1])}мин.  "
                f"({int(budgets_res[2][j+1])}р.)\n\n"
            )
        last_ind = len(names_res) - 1
        msg += f"{cnt}: {names_res[last_ind]} -> центр Москвы\n"
        if times_res[1][-1][1] == 1:
            msg += "🚗  "
        else:
            msg += "🚶  "
        msg += (
            f"в дороге: {int(times_res[1][-1][0])}мин.  "
            f"({int(budgets_res[1][-1])}р.)\n\n"
        )
        msg += f"общее время прогулки: {int(times_res[0])}мин.\n"
        msg += f"общий бюджет: {int(budgets_res[0])}р.\n\n"
        msg += (
            "приятной прогулки, желаю поймать вайб! 🌸\n"
            "если нужен еще один маршрут, просто нажми /start 💘"
        )
        messages.append(msg)

    if final_cnt == 3:
        msg = bot.send_message(
            message.chat.id,
            f'сгнерировал варианты прогулок, выбери один:\n'
            f'1️⃣ {", ".join(str(place) for place in sorted_names[0])}\n'
            f'2️⃣ {", ".join(str(place) for place in sorted_names[1])}\n'
            f'3️⃣ {", ".join(str(place) for place in sorted_names[2])}\n',
            reply_markup=number_3_keyboard()
        )

        def process_choice(msg):
            choices = {"1️⃣": 0, "2️⃣": 1, "3️⃣": 2}
            selected = choices.get(msg.text)
            if selected is None:
                reply = bot.send_message(
                    message.chat.id, "выбери маршрут кнопкой 1️⃣, 2️⃣ или 3️⃣ 🙏🏻"
                )
                bot.register_next_step_handler(reply, process_choice)
                return
            user_history.setdefault(message.chat.id, [])
            if sorted_names[selected] not in user_history[message.chat.id]:
                user_history[message.chat.id].append(sorted_names[selected])
            route_str = ", ".join(str(place) for place in sorted_names[selected])
            msg_text = (
                "прекрасный выбор! вот твой маршрут:\n"
                f"<i>{route_str}</i>\n\n"
            ) + messages[selected]
            bot.send_message(
                message.chat.id,
                msg_text,
                parse_mode="HTML",
                reply_markup=history_keyboard(),
            )

        bot.register_next_step_handler(msg, process_choice)

    else:
        msg = bot.send_message(
            message.chat.id,
            f'сгнерировал варианты прогулок, выбери один:\n'
            f'1️⃣ {", ".join(str(place) for place in sorted_names[0])}\n'
            f'2️⃣ {", ".join(str(place) for place in sorted_names[1])}\n',
            reply_markup=number_2_keyboard()
        )

        def process_choice(msg):
            choices = {"1️⃣": 0, "2️⃣": 1}
            selected = choices.get(msg.text)
            if selected is None:
                reply = bot.send_message(
                    message.chat.id, "выбери маршрут кнопкой 1️⃣ или 2️⃣ 🙏🏻"
                )
                bot.register_next_step_handler(reply, process_choice)
                return

            user_history.setdefault(message.chat.id, [])
            if sorted_names[selected] not in user_history[message.chat.id]:
                user_history[message.chat.id].append(sorted_names[selected])
            route_str = ", ".join(str(place) for place in sorted_names[selected])
            intro = (
                "прекрасный выбор! вот твой маршрут:\n"
                f"<i>{route_str}</i>\n\n"
            )
            msg_text = intro + messages[selected]
            bot.send_message(
                message.chat.id,
                msg_text,
                parse_mode="HTML",
                reply_markup=history_keyboard(),
            )

        bot.register_next_step_handler(msg, process_choice)
