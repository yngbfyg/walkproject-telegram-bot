from utils.route_sort import route_sort
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


route1 = [place3]
route2 = [place1, place2]
route3 = [place1, place3]
routes = [route1, route2, route3]


def test_route_sort():
    tags = ["art", "book"]
    result = route_sort(routes, tags)
    assert result == [1, 0, 2]
