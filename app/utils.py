from datetime import datetime, timedelta
import typing

import pytz

__all__ = "date_scopes", "time_string_as_utc"


def date_scopes(date: str, tz: str):
    assert type(date) == str, "TypeError: date must be a string instance"
    assert type(tz) == str, "TypeError: tz must be a string instance"

    tz = pytz.timezone(tz)
    date = datetime.fromisoformat(date)
    date = tz.localize(date, is_dst=True)
    start_of_day = date.astimezone(pytz.UTC)
    end_of_day = date.astimezone(pytz.UTC) + timedelta(days=1)
    return start_of_day, end_of_day


def time_string_as_utc(time: typing.Union[str, datetime], tz: str):
    assert type(time) in (str, datetime), "TypeError: time must be a string  or datetime instance"
    assert type(tz) == str, "TypeError: tz must be a string instance"
    tz = pytz.timezone(tz)
    time = datetime.fromisoformat(time) if type(time) == str else time
    return tz.localize(time.replace(tzinfo=None), is_dst=True).astimezone(pytz.UTC)
