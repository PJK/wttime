from unittest import TestCase
import time

from wttime.strategy import TimestampStrategy


class TestTimestampStrategy(TestCase):
    def test_parses_int(self):
        self.assertEqual(TimestampStrategy().parse('154'), [1., time.gmtime(154)])
