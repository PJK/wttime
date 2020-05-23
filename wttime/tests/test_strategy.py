from datetime import datetime

from wttime.strategy import SecondsTimestampStrategy, FormatStringStrategy


def _assert_one(actual, expected):
    assert actual == [(100., expected)]


def test_parses_int():
    _assert_one(SecondsTimestampStrategy().parse('154'), datetime.fromtimestamp(154))


def test_parses_dates():
    _assert_one(FormatStringStrategy().parse('2020-08-10'), datetime(2020, 8, 10))
