from datetime import timedelta, datetime
from typing import Tuple, Optional
import math
import dateutil.tz as tz
from datetime import tzinfo

from wttime.strategy import SecondsTimestampStrategy, MillisTimestampStrategy, \
    MicrosTimestampStrategy, FormatStringStrategy, DateutilStrategy


class Parser:
    STRATEGIES = [
        SecondsTimestampStrategy,
        MillisTimestampStrategy,
        MicrosTimestampStrategy,
        FormatStringStrategy,
        DateutilStrategy,
    ]

    @staticmethod
    def parse_tz(spec: str) -> tzinfo:
        timezone = tz.gettz(spec)
        if timezone is None:
            raise ValueError("Couldn't parse timezone spec: " + spec)
        return timezone

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
        - (T, T + 365 days] - linear -> (1, 0.3]
        - (T + 365 days, infty) - half-sigmoid -> (0.3, 0)
        """
        def logcurve(max_value: float, midpoint: float, slope: float, x: float) -> float:
            return max_value / (1 + math.exp(-slope * (x - midpoint)))

        y2k = datetime(2000, 1, 1, tzinfo=tz.tzutc()).timestamp()
        horizon = timedelta(days=365)
        instant_secs = instant.timestamp()

        if instant <= datetime.fromtimestamp(0, tz=tz.tzutc()):
            return logcurve(0.2 * 2, 0, 1. / y2k, instant_secs)
        elif instant <= now:
            return 0.2 + instant_secs / now.timestamp() * 0.8
        elif instant <= now + horizon:
            return 1 - 0.7 * (instant_secs - now.timestamp()) / \
                   horizon.total_seconds()
        else:
            return 0.3 - logcurve(0.3, (now + horizon).timestamp(), 1. / y2k,
                                  instant_secs)

    @staticmethod
    def with_likelihood(now: datetime,
                        parse_result: Tuple[float, datetime]) -> Tuple[float, datetime]:
        confidence, result = parse_result
        return confidence * Parser.instant_likelihood(now, result), result

    def parse(self, now: datetime, timespec: str,
              timezone: tzinfo) -> Optional[Tuple[float, datetime]]:
        parses = []
        for strategy in self.STRATEGIES:
            for parse in strategy(now, timezone).parse(timespec):  # type: ignore
                parses.append(Parser.with_likelihood(now, parse))
        parses.sort(key=lambda g: g[0], reverse=True)
        if parses:
            return parses[0]
        return None
