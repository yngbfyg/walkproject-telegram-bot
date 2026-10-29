"""Модуль для запуска бота."""
import os

import telebot
from dotenv import load_dotenv

from data.time_matrix import time_matrix
from handlers.history import register_history_handlers
from handlers.initial_data import (register_budget_handlers,
                                   register_location_handlers,
                                   register_tags_handlers,
                                   register_walking_time_handlers)
from handlers.start import register_start_handlers
from initial_data_account import initial_places

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)
bot.places = initial_places()
bot.time_matrix = time_matrix
register_start_handlers(bot)
register_budget_handlers(bot)
register_walking_time_handlers(bot)
register_tags_handlers(bot)
register_location_handlers(bot)
register_history_handlers(bot)

if __name__ == "__main__":
    print("Bot started...")
    # print(bot.time_matrix)
    bot.infinity_polling()
