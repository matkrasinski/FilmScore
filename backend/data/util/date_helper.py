from datetime import datetime, timedelta, date


def get_post_update_date(date=datetime.now(), hour=8):
    new_date = date if int(date.strftime(
        "%H")) > hour else date - timedelta(days=1)
    return new_date


def date_from_today(str_date):
    only_date = datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f").date()

    return only_date == date.today()
