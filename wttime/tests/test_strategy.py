from datetime import datetime
import dateutil.tz as tz

from wttime.strategy import SecondsTimestampStrategy, MillisTimestampStrategy, \
    MicrosTimestampStrategy, FormatStringStrategy, DateutilStrategy
from wttime.tests.util import utc_midnight

_NOW = datetime(2020, 3, 1)
_TZ = tz.tzutc()


def _assert_one(actual, expected, expected_confidence=100.):
    assert actual == [(expected_confidence, expected)]


def test_int_strategies():
    _assert_one(SecondsTimestampStrategy(_NOW, _TZ).parse('154'), datetime.fromtimestamp(154, tz=_TZ))

    _assert_one(MillisTimestampStrategy(_NOW, _TZ).parse('154000'), datetime.fromtimestamp(154, tz=_TZ))
    _assert_one(MillisTimestampStrategy(_NOW, _TZ).parse('154001'),
                datetime.fromtimestamp(154, tz=_TZ).replace(microsecond=1000), 90.)

    _assert_one(MicrosTimestampStrategy(_NOW, _TZ).parse('154000000'), datetime.fromtimestamp(154, tz=_TZ))
    _assert_one(MicrosTimestampStrategy(_NOW, _TZ).parse('154000001'),
                datetime.fromtimestamp(154, tz=_TZ).replace(microsecond=1), 90.)

    assert SecondsTimestampStrategy(_NOW, _TZ).parse('hi there') == []


def test_format_string_strategy():
    _assert_one(FormatStringStrategy(_NOW, _TZ).parse('2020-08-10'), utc_midnight(2020, 8, 10))
    _assert_one(FormatStringStrategy(_NOW, _TZ).parse('20200810'), utc_midnight(2020, 8, 10))
    _assert_one(FormatStringStrategy(_NOW, _TZ).parse('10.8.2020'), utc_midnight(2020, 8, 10))

    assert FormatStringStrategy(_NOW, _TZ).parse('quack') == []


def test_dateutil_strategy():
    _assert_one(DateutilStrategy(_NOW, _TZ).parse('2020-08-10'), utc_midnight(2020, 8, 10), 99.)
    _assert_one(DateutilStrategy(_NOW, _TZ).parse('2020-8-10'), utc_midnight(2020, 8, 10), 99.)

    _assert_one(DateutilStrategy(_NOW, _TZ).parse('2020-8-10 02:00:00 -02'),
                datetime(2020, 8, 10, 4, tzinfo=_TZ), 99.)
    _assert_one(DateutilStrategy(_NOW, _TZ).parse('2020-8-10 02:00:00'),
                datetime(2020, 8, 10, 2, tzinfo=_TZ), 99.)

    _assert_one(DateutilStrategy(_NOW, _TZ).parse('Tuesday'), utc_midnight(2020, 3, 3), 99.)
    _assert_one(DateutilStrategy(_NOW, _TZ).parse('Tuesday 9pm'), datetime(2020, 3, 3, 21, tzinfo=_TZ), 99.)

    _assert_one(DateutilStrategy(_NOW, _TZ).parse('Monday 2020-8-10'), utc_midnight(2020, 8, 10), 99.)
    # WAI but dangerous
    _assert_one(DateutilStrategy(_NOW, _TZ).parse('Tuesday 2020-8-10'), utc_midnight(2020, 8, 10), 99.)
    _assert_one(DateutilStrategy(_NOW, _TZ).parse('Notaday 2020-8-10'), utc_midnight(2020, 8, 10), 49.5)
    _assert_one(DateutilStrategy(_NOW, _TZ).parse('Notaday 2020-8-10, etc'),
                utc_midnight(2020, 8, 10), 24.75)
