from unittest import TestCase
from datetime import datetime

from wttime.strategy import TimestampStrategy


class TestTimestampStrategy(TestCase):
    def test_parses_int(self):
        self.assertEqual(TimestampStrategy().parse('154'),
                         [1., datetime.fromtimestamp(154)])
