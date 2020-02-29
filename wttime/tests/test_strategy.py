from unittest import TestCase
from datetime import datetime

from wttime.strategy import SecondsTimestampStrategy


class TestSecondsTimestampStrategy(TestCase):
    def test_parses_int(self):
        self.assertEqual(SecondsTimestampStrategy().parse('154'),
                         [100., datetime.fromtimestamp(154)])
