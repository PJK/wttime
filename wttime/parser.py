from typing import Tuple, Optional, NewType
from time import gmtime, struct_time, time, mktime
from datetime import timedelta, datetime
import math

from wttime.strategy import TimestampStrategy


class Parser:
    strategies = [
        TimestampStrategy()
    ]

    @staticmethod
    def instant_likelihood(now: datetime, instant: datetime) -> float:
        """Given a time, estimates the likelihood (0, 1] that this is a real
        timestamp.

        The following assumptions are used:
        - Most timestamps are in the past by the point they are inspected
        - Most timestamps of interest are in the recent past
        - Timestamps before epoch are unlikely in computer systems
        - Dates in the future are likely relatively close (TTLs, durations)

        This is implemented as a combination of linear and logistic functions:
        - (-infty, epoch start] - half-sigmoid -> (0, 0.2]
        - (epoch start, T] - linear -> (0.2, 1]
        - (T, T + 60 days] - linear -> (1, 0.3]
        - (T + 60 days, infty) - half-sigmoid -> (0.3, 0)
        """

        def logcurve(max_value, midpoint, slope, x):
            return max_value / (1 + math.exp(-slope * (x - midpoint)))

        y2k = datetime(2000, 1, 1).timestamp()
        horizon = timedelta(days=60)
        instant_secs = instant.timestamp()

        if instant <= datetime.fromtimestamp(0):
            return logcurve(0.2 * 2, 0, 1. / y2k, instant_secs)
        elif instant <= now:
            return 0.2 + instant_secs / now.timestamp() * 0.8
        elif instant <= now + horizon:
            return 1 - 0.7 * (instant_secs - now.timestamp()) / \
                   horizon.total_seconds()
        else:
            return 1 - logcurve((1 - 0.3) * 2,
                                (now + horizon).timestamp(),
                                1. / y2k,
                                instant_secs)

    @staticmethod
    def with_likelihood(now: datetime, parse_result):
        if parse_result:
            confidence, result = parse_result
            return confidence * Parser.instant_likelihood(now, result), result

    def parse(self, now, timespec):
        parses = [Parser.with_likelihood(now, strategy.parse(timespec)) for
                  strategy in self.strategies]
        guesses = list(filter(None, parses))
        guesses.sort(key=lambda g: g[0], reverse=True)
        if guesses:
            return guesses[0]
