from datetime import datetime

from wttime.cli import CLI
from wttime.parser import Parser

_TZ = Parser.parse_tz('America/New_York')
_CLI = CLI(Parser(datetime(2020, 2, 1), _TZ), _TZ, True, True, True, True,
           Parser.parse_tz('America/Los_Angeles'), '%Y-%m-%d %H:%M:%S (%z)',
           True, True, True, True)


def test_format_parse():
    res = _CLI.format_parse(95., datetime(2020, 3, 1, 22, 35, 1, 5, _TZ))
    assert res == \
           """Confidence: 95.0000000000
UTC:     2020-03-02 03:35:01 (+0000)
Local:   2020-03-01 22:35:01 (-0500)
Remote:  2020-03-01 19:35:01 (-0800)
Seconds: 1583120101
Millis:  1583120101000
Micros:  1583120101000005"""
