import pytest

from utils.time_conv import minutes_since_midnight


def test_minutes_since_midnight():
    assert minutes_since_midnight("20:34") == 20 * 60 + 34
