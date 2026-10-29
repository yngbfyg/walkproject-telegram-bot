from utils.travel_time import safe_get
from unittest.mock import patch, Mock
from utils.travel_time import get_travel_time
from utils.travel_time import get_time_matrix
from core.models import PlaceDTO


@patch("utils.travel_time.requests.get")
def test_safe_get_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    url = "smth"
    response = safe_get(url)

    assert response == mock_response
    mock_get.assert_called_once_with(url)


@patch("utils.travel_time.time.sleep")
@patch("utils.travel_time.requests.get")
def test_safe_get_retries_on_429(mock_get, mock_sleep):
    response_429 = Mock(status_code=429, headers={"Retry-After": "1"})
    response_429.raise_for_status.side_effect = None
    response_200 = Mock(status_code=200)
    response_200.raise_for_status.return_value = None

    mock_get.side_effect = [response_429, response_429, response_200]

    url = "smth"
    response = safe_get(url)

    assert response == response_200
    assert mock_get.call_count == 3
    assert mock_sleep.call_count == 2


@patch("utils.travel_time.safe_get")
def test_get_travel_time_walk(mock_safe_get):
    # пешком занимает 10 минут
    mock_response = Mock()
    mock_response.json.return_value = {"paths": [{"time": 10 * 60 * 1000}]}
    mock_safe_get.return_value = mock_response

    origin = (55.75, 37.61)
    destination = (55.76, 37.62)

    result = get_travel_time(origin, destination)

    assert result == (10.0, 0)
    mock_safe_get.assert_called_once()


@patch("utils.travel_time.safe_get")
def test_get_travel_time_switch_to_car(mock_safe_get):
    walk_resp = Mock()
    walk_resp.json.return_value = {"paths": [{"time": 26 * 60 * 1000}]}

    car_resp = Mock()
    car_resp.json.return_value = {"paths": [{"time": 7 * 60 * 1000}]}

    mock_safe_get.side_effect = [walk_resp, car_resp]

    origin = (55.75, 37.61)
    destination = (55.80, 37.65)

    result = get_travel_time(origin, destination)

    assert result == (12.0, 1)
    assert mock_safe_get.call_count == 2


@patch("utils.travel_time.time.sleep")
@patch("utils.travel_time.get_travel_time")
def test_get_time_matrix(mock_get_travel_time, mock_sleep):
    mock_get_travel_time.return_value = (12.5, 0)

    places = [
        PlaceDTO(
            name="A",
            lat=55.75,
            lon=37.61,
            category="",
            price=0,
            tags=[],
            avg_visit_time=0,
            weather="",
            work_time_dict={},
        ),
        PlaceDTO(
            name="B",
            lat=55.76,
            lon=37.62,
            category="",
            price=0,
            tags=[],
            avg_visit_time=0,
            weather="",
            work_time_dict={},
        ),
        PlaceDTO(
            name="C",
            lat=55.77,
            lon=37.63,
            category="",
            price=0,
            tags=[],
            avg_visit_time=0,
            weather="",
            work_time_dict={},
        ),
    ]

    result = get_time_matrix(places)

    assert len(result) == 3
    assert all(len(row) == 3 for row in result)

    for i in range(3):
        for j in range(3):
            if i == j:
                assert result[i][j] == (0.0, 0)
            else:
                assert result[i][j] == (12.5, 0)

    assert mock_get_travel_time.call_count == 3
    assert mock_sleep.call_count == 3
