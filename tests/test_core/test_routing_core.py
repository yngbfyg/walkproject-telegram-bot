from core.models import PlaceDTO
from core.routing import one_walk_budget, route_budget, route_time, generate_route

w_one_minute_ride = 8

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

start = (55.764394, 37.598420)

time_matrix = [
    [(0.0, 0), (80.06635, 1), (20.0238, 0), (12.584283333333333, 1)],
    [(80.06635, 1), (0.0, 0), (17.771099999999997, 1), (19.422116666666668, 1)],
    [(20.0238, 1), (15.07235, 1), (0.0, 0), (16.483583333333335, 1)],
    [(12.584283333333333, 1), (15.800233333333333, 1), (18.25595, 1), (0.0, 0)],
]


def test_one_walk_budget():
    assert (
        one_walk_budget(time_matrix, 0, 1) == time_matrix[0][1][0] * w_one_minute_ride
    )
    assert one_walk_budget(time_matrix, 0, 2) == 0


def test_route_budget():
    budget_start_place1 = one_walk_budget(time_matrix, 0, 1)
    budget_place1_place2 = one_walk_budget(time_matrix, 1, 2)
    budget_place2_start = one_walk_budget(time_matrix, 2, 0)
    assert route_budget([1, 2], places, time_matrix) == (
        900 + 300 + budget_start_place1 + budget_place1_place2 + budget_place2_start,
        [budget_start_place1, budget_place1_place2, budget_place2_start],
        [300, 900],
    )
    assert route_budget([], places, time_matrix) == 0


def test_route_time():
    time_start_place1 = time_matrix[0][1]
    time_place1_place2 = time_matrix[1][2]
    time_place2_start = time_matrix[2][0]
    assert route_time([1, 2], places, time_matrix) == (
        60 + 80 + time_start_place1[0] + time_place1_place2[0] + time_place2_start[0],
        [time_start_place1, time_place1_place2, time_place2_start],
        [60, 80],
    )
    assert route_time([], places, time_matrix) == 0


def test_generate_route():
    assert generate_route(
        places, 12 * 60, "outdoor", "wed", 500, 250, ["art"], time_matrix
    ) == (
        [place3],
        route_time([3], places, time_matrix),
        route_budget([3], places, time_matrix),
    )
    assert generate_route(
        places, 12 * 60, "outdoor", "wed", 2200, 200, ["vegan"], time_matrix
    ) == (
        [place2],
        route_time([2], places, time_matrix),
        route_budget([2], places, time_matrix),
    )
