from datetime import datetime, timedelta
import typing

import pytz


def date_scopes(date: str, tz: str):
    assert type(date) == str, "TypeError: date must be a string instance"
    assert type(tz) == str, "TypeError: tz must be a string instance"

    tz = pytz.timezone(tz)

    date = datetime.fromisoformat(date).astimezone(tz)
    start_of_day = date.astimezone(pytz.UTC)
    end_of_day = date.astimezone(pytz.UTC) + timedelta(days=1)
    return start_of_day, end_of_day


def time_string_as_utc(time: typing.Union[str, datetime], tz: str):
    assert type(time) in (str, datetime), "TypeError: time must be a string  or datetime instance"
    assert type(tz) == str, "TypeError: tz must be a string instance"
    tz = pytz.timezone(tz)
    if type(time) == str:
        time = datetime.fromisoformat(time)
    else:
        time = time.replace(tzinfo=None)
    time = tz.localize(time)
    utc = time.astimezone(pytz.UTC)
    return utc


def convert_to_timezone(time: typing.Union[datetime, str], tz: str):
    """Converts a string or datetime object to the desired timezone."""

    # Type checking
    assert type(tz) == str, "TypeError: timezone must be a string instance"
    assert type(time) in [datetime, str], "TypeError: time must be a string or datetime instance"

    # Conversions
    tz = pytz.timezone(tz)
    if type(time) == str:
        time = datetime.fromisoformat(time)

    # Replace provided time's timezone with UTC
    utc_time = time.replace(tzinfo=pytz.UTC)

    # Localize UTCed time
    localized = utc_time.astimezone(tz)

    return localized
