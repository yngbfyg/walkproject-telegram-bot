from services.weather import get_current_weather
from unittest.mock import patch


@patch("services.weather.requests.get")
def test_get_current_weather(mock_get):
    fake_response = {
        "current": {
            "temp_c": 21.5,
            "condition": {"text": "снег"},
            "wind_kph": 10.8,
            "humidity": 48,
        }
    }

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = fake_response

    lat, lon = 55.75, 37.61
    result = get_current_weather(lat, lon)

    assert result == {
        "temp_c": 21.5,
        "condition": "снег",
        "wind_kph": 10.8,
        "humidity": 48,
    }

    mock_get.assert_called_once()
