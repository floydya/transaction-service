from datetime import datetime

from django.test import TestCase
from app.utils import time_string_as_utc, date_scopes


class UtilsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.timezone = "Europe/Kiev"
        cls.date_string = "2020-02-01"
        cls.datetime_string = "2020-02-01T00:00:00"
        cls.datetime = datetime(2020, 2, 1)

    def test_time_string_as_utc(self):
        try:
            time_string_as_utc(1, 1)
            self.fail()
        except AssertionError as e:
            self.assertEqual(str(e), "TypeError: time must be a string  or datetime instance")

        try:
            time_string_as_utc(self.datetime_string, 1)
            self.fail()
        except AssertionError as e:
            self.assertEqual(str(e), "TypeError: tz must be a string instance")

        try:
            time_string_as_utc(self.datetime, 1)
            self.fail()
        except AssertionError as e:
            self.assertEqual(str(e), "TypeError: tz must be a string instance")

    def test_time_string_as_utc_winter(self):
        utc_datetime = "2020-01-31T22:00:00+00:00"
        result1 = time_string_as_utc(self.datetime_string, self.timezone).isoformat()
        result2 = time_string_as_utc(self.datetime, self.timezone).isoformat()
        self.assertEqual(result1, utc_datetime)
        self.assertEqual(result2, utc_datetime)

    def test_time_string_as_utc_summer(self):
        _datetime_string = "2020-07-01T00:00:00"
        _datetime = datetime(2020, 7, 1)

        utc_datetime = "2020-06-30T21:00:00+00:00"
        result1 = time_string_as_utc(_datetime_string, self.timezone).isoformat()
        result2 = time_string_as_utc(_datetime, self.timezone).isoformat()
        self.assertEqual(result1, utc_datetime)
        self.assertEqual(result2, utc_datetime)

    def test_date_scopes(self):
        try:
            date_scopes(1, 1)
            self.fail()
        except AssertionError as e:
            self.assertEqual(str(e), "TypeError: date must be a string instance")

        try:
            date_scopes(self.date_string, 1)
            self.fail()
        except AssertionError as e:
            self.assertEqual(str(e), "TypeError: tz must be a string instance")

    def test_date_scopes_winter(self):
        expected_result = ("2020-01-31T22:00:00+00:00", "2020-02-01T22:00:00+00:00")
        result = tuple(a.isoformat() for a in date_scopes(self.date_string, self.timezone))
        self.assertEqual(expected_result, result)

    def test_date_scopes_summer(self):
        date_string = "2020-07-01"
        expected_result = ("2020-06-30T21:00:00+00:00", "2020-07-01T21:00:00+00:00")
        result = tuple(a.isoformat() for a in date_scopes(date_string, self.timezone))
        self.assertEqual(expected_result, result)
