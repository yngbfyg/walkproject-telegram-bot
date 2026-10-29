"""Regression tests for routes without enough valid candidate itineraries.

The Telegram UI dependency is stubbed so these guard tests run offline.
"""
import importlib
import sys
import types
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest


@pytest.fixture
def route_handler(monkeypatch):
    fake_telebot = types.ModuleType("telebot")
    fake_types = types.ModuleType("telebot.types")

    class FakeKeyboard:
        def __init__(self, **kwargs):
            pass

        def add(self, *args):
            pass

    fake_telebot.TeleBot = object
    fake_types.Message = object
    fake_types.KeyboardButton = lambda *a, **k: object()
    fake_types.ReplyKeyboardMarkup = FakeKeyboard
    monkeypatch.setitem(sys.modules, "telebot", fake_telebot)
    monkeypatch.setitem(sys.modules, "telebot.types", fake_types)

    # Import from the repository under test, without requiring a bot token.
    old = sys.modules.pop("handlers.route", None)
    old_keyboard = sys.modules.pop("keyboards.reply_keyboard", None)
    try:
        route = importlib.import_module("handlers.route")
        yield route
    finally:
        sys.modules.pop("handlers.route", None)
        sys.modules.pop("keyboards.reply_keyboard", None)
        if old is not None:
            sys.modules["handlers.route"] = old
        if old_keyboard is not None:
            sys.modules["keyboards.reply_keyboard"] = old_keyboard


def prepare_session(route, chat_id):
    route.user_data[chat_id] = {
        "location": {"lat": 55.75, "lon": 37.62},
        "budget": 500,
        "time": 120,
        "tags": ["art"],
    }
    return SimpleNamespace(chat=SimpleNamespace(id=chat_id))


def test_no_routes_returns_without_choice_keyboard(route_handler):
    route = route_handler
    message = prepare_session(route, 17051)
    bot = Mock()
    with patch.object(route, "get_type_weather", return_value="outdoor"), \
            patch.object(route, "generate_route", return_value=([], 0, 0)):
        route.send_route(bot, message)

    bot.send_message.assert_called_once()
    assert "попробуй еще раз" in bot.send_message.call_args.args[1]
    bot.register_next_step_handler.assert_not_called()
    route.user_data.pop(message.chat.id, None)


def test_one_valid_route_is_handled_gracefully(route_handler):
    route = route_handler
    message = prepare_session(route, 17052)
    bot = Mock()
    only_place = SimpleNamespace(name="Museum")
    one_route = ([only_place], (60, [], []), (0, [], []))
    outcomes = [([], 0, 0)] * 14 + [one_route]
    with patch.object(route, "get_type_weather", return_value="outdoor"), \
            patch.object(route, "generate_route", side_effect=outcomes):
        route.send_route(bot, message)

    bot.send_message.assert_called_once()
    bot.register_next_step_handler.assert_not_called()
    route.user_data.pop(message.chat.id, None)
