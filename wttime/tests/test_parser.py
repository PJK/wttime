from datetime import timedelta
import pytest

from wttime.tests.util import utc_midnight
from wttime.parser import Parser


def test_instant_likelihood():
    def likelihood(date):
        return Parser.instant_likelihood(utc_midnight(2019, 1, 1), date)

    assert likelihood(utc_midnight(1500, 1, 1)) < 0.2
    assert likelihood(utc_midnight(1970, 1, 1)) == pytest.approx(0.2, abs=1e4)
    assert 0.2 < likelihood(utc_midnight(1990, 1, 1)) <= 1
    assert likelihood(utc_midnight(2019, 1, 1)) == pytest.approx(0.2, abs=1e4)
    assert 1 > likelihood(utc_midnight(2019, 2, 1)) >= 0.3
    assert likelihood(utc_midnight(2019, 1, 1) +
                      timedelta(days=60)) == pytest.approx(0.3, abs=1e4)
    assert likelihood(utc_midnight(2050, 1, 1)) < 0.3
