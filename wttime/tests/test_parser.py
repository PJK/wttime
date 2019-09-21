from unittest import TestCase
from datetime import datetime, timedelta

from wttime.parser import Parser

class TestParser(TestCase):
    def test_instant_likelihood(self):
        reference = datetime(2019, 1, 1)
        self.assertLess(
            Parser.instant_likelihood(reference, datetime(1500, 1, 1)),
            0.2)
        self.assertAlmostEqual(
            Parser.instant_likelihood(reference, datetime(1970, 1, 1)),
            0.2,
            places=5)
        self.assertTrue(
            0.2 < Parser.instant_likelihood(reference,
                                            datetime(1990, 1, 1)) <= 1)
        self.assertAlmostEqual(
            Parser.instant_likelihood(reference, reference), 1)
        self.assertTrue(
            1 > Parser.instant_likelihood(reference,
                                            datetime(2019, 2, 1)) >= 0.3)
        self.assertAlmostEqual(
            Parser.instant_likelihood(
                reference,
                datetime(2019, 1, 1) + timedelta(days=60)),
            0.3)
        self.assertLess(
            Parser.instant_likelihood(reference, datetime(2050, 1, 1)), 0.3)