from unittest.mock import patch
from utils.weather import get_type_weather


@patch("utils.weather.get_current_weather")
def test_get_type_weather_cold(mock_get_weather):
    start = (55.75, 37.61)
    mock_get_weather.return_value = {
        "temp_c": 0.0,
        "condition": "",
        "wind_kph": 5,
        "humidity": 40,
    }
    result = get_type_weather(start)
    assert result == "indoor"
    mock_get_weather.assert_called_once()


@patch("utils.weather.get_current_weather")
def test_get_type_weather_snow(mock_get_weather):
    start = (55.75, 37.61)
    mock_get_weather.return_value = {
        "temp_c": 20.0,
        "condition": "снег",
        "wind_kph": 5,
        "humidity": 40,
    }
    result = get_type_weather(start)
    assert result == "indoor"
    mock_get_weather.assert_called_once()


@patch("utils.weather.get_current_weather")
def test_get_type_weather_outdoor(mock_get_weather):
    start = (55.75, 37.61)
    mock_get_weather.return_value = {
        "temp_c": 20.0,
        "condition": "",
        "wind_kph": 5,
        "humidity": 40,
    }
    result = get_type_weather(start)
    assert result == "outdoor"
    mock_get_weather.assert_called_once()


@patch("utils.weather.get_current_weather")
def test_get_type_weather_wind(mock_get_weather):
    start = (55.75, 37.61)
    mock_get_weather.return_value = {
        "temp_c": 20.0,
        "condition": "",
        "wind_kph": 15,
        "humidity": 40,
    }
    result = get_type_weather(start)
    assert result == "indoor"
    mock_get_weather.assert_called_once()
