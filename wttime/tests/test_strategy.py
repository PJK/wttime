from datetime import datetime

from wttime.strategy import *

_NOW = datetime(2020, 3, 1)


def _assert_one(actual, expected, expected_confidence=100.):
    assert actual == [(expected_confidence, expected)]


def test_int_strategies():
    _assert_one(SecondsTimestampStrategy(_NOW).parse('154'), datetime.fromtimestamp(154))

    _assert_one(MillisTimestampStrategy(_NOW).parse('154000'), datetime.fromtimestamp(154))
    _assert_one(MillisTimestampStrategy(_NOW).parse('154001'),
                datetime.fromtimestamp(154).replace(microsecond=1000), 90.)

    _assert_one(MicrosTimestampStrategy(_NOW).parse('154000000'), datetime.fromtimestamp(154))
    _assert_one(MicrosTimestampStrategy(_NOW).parse('154000001'),
                datetime.fromtimestamp(154).replace(microsecond=1), 90.)

    assert SecondsTimestampStrategy(_NOW).parse('hi there') == []


def test_format_string_strategy():
    _assert_one(FormatStringStrategy(_NOW).parse('2020-08-10'), datetime(2020, 8, 10))
    _assert_one(FormatStringStrategy(_NOW).parse('20200810'), datetime(2020, 8, 10))
    _assert_one(FormatStringStrategy(_NOW).parse('10.8.2020'), datetime(2020, 8, 10))

    assert FormatStringStrategy(_NOW).parse('quack') == []


def test_dateutil_strategy():
    _assert_one(DateutilStrategy(_NOW).parse('2020-08-10'), datetime(2020, 8, 10), 99.)
    _assert_one(DateutilStrategy(_NOW).parse('2020-8-10'), datetime(2020, 8, 10), 99.)

    _assert_one(DateutilStrategy(_NOW).parse('Tuesday'), datetime(2020, 3, 3), 99.)
    _assert_one(DateutilStrategy(_NOW).parse('Tuesday 9pm'), datetime(2020, 3, 3, 21), 99.)

    _assert_one(DateutilStrategy(_NOW).parse('Monday 2020-8-10'), datetime(2020, 8, 10), 99.)
    # WAI but dangerous
    _assert_one(DateutilStrategy(_NOW).parse('Tuesday 2020-8-10'), datetime(2020, 8, 10), 99.)
    _assert_one(DateutilStrategy(_NOW).parse('Notaday 2020-8-10'), datetime(2020, 8, 10), 49.5)
    _assert_one(DateutilStrategy(_NOW).parse('Notaday 2020-8-10, etc'),
                datetime(2020, 8, 10), 24.75)
