from core.evaluation import init_filter_places
from core.evaluation import filter_places_by_tags
from core.evaluation import filter_places_by_weather
from core.evaluation import filter_places_by_dist
from core.evaluation import filter_places_by_budget
from core.evaluation import filter_places
from core.evaluation import filter_places_without_tags
from core.models import PlaceDTO

place1 = PlaceDTO(
    name="Ботанический сад МГУ Аптекарский огород",
    lat=55.777600,
    lon=37.635061,
    category="парк",
    price=300,
    tags=["park", "botanic-garden"],
    avg_visit_time=60,
    weather="outdoor",
    work_time_dict={
        "mon": ("10:00", "20:30"),
        "tue": ("10:00", "20:30"),
        "wed": ("10:00", "20:30"),
        "thu": ("10:00", "20:30"),
        "fri": ("10:00", "20:30"),
        "sat": ("10:00", "20:30"),
        "sun": ("10:00", "20:30"),
    },
)

place2 = PlaceDTO(
    name="Мох веганское кафе",
    lat=55.752180,
    lon=37.668949,
    category="кафе",
    price=900,
    tags=["vegan"],
    avg_visit_time=80,
    weather="indoor",
    work_time_dict={
        "mon": ("12:00", "23:00"),
        "tue": ("12:00", "23:00"),
        "wed": ("12:00", "23:00"),
        "thu": ("12:00", "23:00"),
        "fri": ("12:00", "23:00"),
        "sat": ("11:00", "23:00"),
        "sun": ("11:00", "23:00"),
    },
)

place3 = PlaceDTO(
    name="Дом культуры «ГЭС-2»",
    lat=55.74270259704878,
    lon=37.6129383685587,
    category="культруное пространство",
    price=0,
    tags=["art", "book"],
    avg_visit_time=90,
    weather="indoor",
    work_time_dict={
        "mon": ("11:00", "22:00"),
        "tue": ("11:00", "22:00"),
        "wed": ("11:00", "22:00"),
        "thu": ("11:00", "22:00"),
        "fri": ("11:00", "22:00"),
        "sat": ("11:00", "22:00"),
        "sun": ("11:00", "22:00"),
    },
)

places = [place1, place2, place3]

time_matrix = [
    [(0.0, 0), (80.06635, 1), (20.0238, 1), (12.584283333333333, 1)],
    [(80.06635, 1), (0.0, 0), (17.771099999999997, 1), (19.422116666666668, 1)],
    [(20.0238, 1), (15.07235, 1), (0.0, 0), (16.483583333333335, 1)],
    [(12.584283333333333, 1), (15.800233333333333, 1), (18.25595, 1), (0.0, 0)],
]

fake_time_matrix = [
    [(0.0, 0), (0.0, 0), (0.0, 0), (0.0, 0)],
    [(0.0, 0), (0.0, 0), (0.0, 0), (0.0, 0)],
    [(0.0, 0), (0.0, 0), (0.0, 0), (0.0, 0)],
    [(0.0, 0), (0.0, 0), (0.0, 0), (0.0, 0)],
]

start = (55.764394, 37.598420)


def test_init_filter_places():
    assert init_filter_places(places) == [0, 1, 2]


def test_filter_places_by_tags():
    filterplaces = filter_places_by_tags(places, ["art"], [0, 1, 2])
    assert filterplaces == [2]


def test_filter_places_by_weather_indoor():
    filterplaces = filter_places_by_weather(places, "indoor", [0, 1, 2])
    assert filterplaces == [1, 2]


def test_filter_places_by_weather_outdoor():
    filterplaces = filter_places_by_weather(places, "outdoor", [0, 1, 2])
    assert filterplaces == [0, 1, 2]


def test_filter_places_by_dist():
    filterplaces = filter_places_by_dist(200, time_matrix, [0, 1, 2])
    assert filterplaces == [1, 2]


def test_filter_places_by_budget():
    filterplaces = filter_places_by_budget(places, 100, [0, 1, 2])
    assert filterplaces == [2]


def test_filter_places():
    filterplaces = filter_places(places, 200, 700, ["vegan"], "indoor", time_matrix)
    assert filterplaces == []


def test_filter_places_without_tags():
    filterplaces = filter_places_without_tags(places, 200, 700, "indoor", time_matrix)
    assert filterplaces == [3]
