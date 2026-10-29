from core.models import PlaceDTO
from data.parser import parse_line

place = PlaceDTO(
    name="ботанический сад МГУ Аптекарский огород",
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


def test_parse_line():
    line = (
        "ботанический сад МГУ Аптекарский огород, "
        "55.777600, 37.635061, "
        "парк, 300, "
        '["park", "botanic-garden"], '
        "60, outdoor, "
        '{"mon": ("10:00", "20:30"), '
        '"tue": ("10:00", "20:30"), '
        '"wed": ("10:00", "20:30"), '
        '"thu": ("10:00", "20:30"), '
        '"fri": ("10:00", "20:30"), '
        '"sat": ("10:00", "20:30"), '
        '"sun": ("10:00", "20:30")}'
    )
    assert parse_line(line) == place
