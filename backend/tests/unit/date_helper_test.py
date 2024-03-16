from ...data.util.date_helper import *
from datetime import datetime


def test_not_today_date():
    date = datetime(year=2024, month=2, day=2, hour=16)
    date = get_post_update_date(date, 17)

    assert date == datetime(year=2024, month=2, day=1, hour=16)


def test_test_today_date():
    date = datetime(year=2024, month=2, day=2, hour=18)
    date = get_post_update_date(date, 17)

    assert date == datetime(year=2024, month=2, day=2, hour=18)
