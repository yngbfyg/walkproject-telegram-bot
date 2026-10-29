"""The bot should ask again instead of crashing on invalid numeric replies."""
import importlib
import sys
import types
from types import SimpleNamespace

import pytest


@pytest.fixture
def input_handlers(monkeypatch):
    fake_bot = types.ModuleType("telebot")
    fake_types = types.ModuleType("telebot.types")

    class FakeKeyboard:
        def __init__(self, **kwargs):
            pass

        def add(self, *args):
            pass

    fake_bot.TeleBot = object
    fake_types.Message = object
    fake_types.KeyboardButton = lambda *args, **kwargs: object()
    fake_types.ReplyKeyboardMarkup = FakeKeyboard
    monkeypatch.setitem(sys.modules, "telebot", fake_bot)
    monkeypatch.setitem(sys.modules, "telebot.types", fake_types)

    old_handlers = sys.modules.pop("handlers.initial_data", None)
    old_route = sys.modules.pop("handlers.route", None)
    old_keyboard = sys.modules.pop("keyboards.reply_keyboard", None)
    try:
        imported = importlib.import_module("handlers.initial_data")
        yield imported
    finally:
        for name, old in [
            ("handlers.initial_data", old_handlers),
            ("handlers.route", old_route),
            ("keyboards.reply_keyboard", old_keyboard),
        ]:
            sys.modules.pop(name, None)
            if old is not None:
                sys.modules[name] = old


class FakeConversationBot:
    def __init__(self):
        self.button_handler = None
        self.next_handler = None
        self.sent = []

    def message_handler(self, **kwargs):
        def register(callback):
            self.button_handler = callback
            return callback
        return register

    def send_message(self, chat_id, text, **kwargs):
        self.sent.append(text)
        return SimpleNamespace(chat=SimpleNamespace(id=chat_id), text=text)

    def register_next_step_handler(self, message, callback):
        self.next_handler = callback


@pytest.mark.parametrize("kind,bad,good", [
    ("budget", "бесплатно", "1000"),
    ("budget", "-20", "0"),
    ("budget", None, "500"),
    ("time", "долго", "250"),
    ("time", "0", "30"),
    ("time", "-30", "90"),
])
def test_invalid_numbers_are_reprompted(input_handlers, kind, bad, good):
    bot = FakeConversationBot()
    register = (input_handlers.register_budget_handlers if kind == "budget"
                else input_handlers.register_walking_time_handlers)
    register(bot)
    chat_id = 4183
    msg = lambda text: SimpleNamespace(chat=SimpleNamespace(id=chat_id), text=text)
    input_handlers.user_data.pop(chat_id, None)
    try:
        bot.button_handler(msg("🤑 бюджет" if kind == "budget" else "⏱️ время прогулки"))
        bot.next_handler(msg(bad))
        assert "введи" in bot.sent[-1]
        assert kind not in input_handlers.user_data.get(chat_id, {})
        bot.next_handler(msg(good))
        assert input_handlers.user_data[chat_id][kind] == int(good)
        assert "супии" in bot.sent[-1]
    finally:
        input_handlers.user_data.pop(chat_id, None)

