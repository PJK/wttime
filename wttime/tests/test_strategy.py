from datetime import datetime

from wttime.strategy import SecondsTimestampStrategy


def test_parses_int():
    parse = SecondsTimestampStrategy().parse('154')
    assert parse == [100., datetime.fromtimestamp(154)]
