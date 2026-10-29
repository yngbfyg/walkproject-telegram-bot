from unittest.mock import patch
from services.routing import get_travel_time_graphhopper


@patch("services.routing.requests.get")
def test_get_travel_time_graphhopper(mock_get):
    fake_response = {"paths": [{"time": 120000}]}
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = fake_response

    origin = (55.751244, 37.618423)
    destination = (55.7558, 37.6173)

    travel_time = get_travel_time_graphhopper(origin, destination, "car")

    assert travel_time == 2.0
    mock_get.assert_called_once()
