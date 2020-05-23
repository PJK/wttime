from datetime import datetime, tzinfo
from abc import ABC, abstractmethod
from typing import Tuple, List
from dateutil.parser import parse as du_parse


class Strategy(ABC):
    def __init__(self, now: datetime, timezone: tzinfo):
        self.now = now
        self.timezone = timezone

    """Parses a string into a datetime and assigns it a confidence level.

    TODO: This design is completely arbitrary and the first thing that came
          to my mind.
    Confidence level guidance:
    (-infty, 0]
        Bad parse (consider returning no result)
    (0, 25]
        Unlikely fuzzy match; some fixing/coercion has been applied
    (25, 50]
        Likely fuzzy match; a common fix/coercion has been applied (e.g. a
        common typo has been fixed)
    (50, 100]
        Exact match; the input exactly fits the pattern
    (100, infty)
        Special cases + headroom for hacks and overrides


    TODO: Allow users to prefer/pick/override strategies via labels
    TODO: Think about better way to prevent weird interactions and endless
          global tweaking
    TODO: Maybe we should be able to return multiple parses from a single
          strategy?
    TODO: Maybe strategies should have a finite number of confidences so that
          we can enumerate all the comparisons?
    TODO: Probably strategies themselves should be weighted based on the
          frequency of use?
    """
    @abstractmethod
    def parse(self, timespec: str) -> List[Tuple[float, datetime]]:
        pass


class TimestampStrategy(Strategy):
    @abstractmethod
    def parse_timestamp(self, timestamp: float) -> Tuple[float, datetime]:
        pass

    def parse(self, timespec: str) -> List[Tuple[float, datetime]]:
        try:
            # TODO: Handle non-decimals etc.
            return [self.parse_timestamp(float(timespec))]
        except ValueError:
            return []


class SecondsTimestampStrategy(TimestampStrategy):
    def parse_timestamp(self, timestamp: float) -> Tuple[float, datetime]:
        # Most second timestamps are integers
        return (
            100. if int(timestamp) == timestamp else 70.,
            datetime.fromtimestamp(timestamp, tz=self.timezone)
        )


class MillisTimestampStrategy(TimestampStrategy):
    def parse_timestamp(self, timestamp: float) -> Tuple[float, datetime]:
        # Prefer integers, prefer multiples of 1000
        if int(timestamp) == timestamp:
            confidence = 100. if timestamp % 1e3 == 0 else 90.
        else:
            confidence = 70.

        return confidence, datetime.fromtimestamp(timestamp / 1e3, tz=self.timezone)


class MicrosTimestampStrategy(TimestampStrategy):
    def parse_timestamp(self, timestamp: float) -> Tuple[float, datetime]:
        # Prefer integers, prefer multiples of 1000000
        if int(timestamp) == timestamp:
            confidence = 100. if timestamp % 1e6 == 0 else 90.
        else:
            confidence = 70.

        return confidence, datetime.fromtimestamp(timestamp / 1e6, tz=self.timezone)


class FormatStringStrategy(Strategy):
    COMMON_FORMATS = [
        '%Y%m%d',
        '%Y-%m-%d',
        '%d.%m.%Y',
    ]

    def parse(self, timespec: str) -> List[Tuple[float, datetime]]:
        parses = []
        for fmt in self.COMMON_FORMATS:
            try:
                parses.append((100.,
                               datetime.strptime(timespec, fmt).replace(tzinfo=self.timezone)))
            except ValueError:
                pass
        return parses


class DateutilStrategy(Strategy):
    def parse(self, timespec: str) -> List[Tuple[float, datetime]]:
        try:
            # TODO: This clipping is suboptimal, e.g. 2020 should probably be 2020-01-01, but
            # 'Tuesday' should still be pinned to the current date. Find out the actual parse
            # spec used and adjust
            reference = self.now.replace(hour=0, minute=0, second=0, microsecond=0,
                                         tzinfo=self.timezone)
            parse: datetime
            skipped: Tuple[str]
            parse, skipped = du_parse(timespec,   # type: ignore
                                      default=reference, fuzzy=True,
                                      fuzzy_with_tokens=True)
            # Slightly discount magic w.r.t. FormatStringStrategy, ignore single whitespaces
            confidence = (1/2) ** len([tok for tok in skipped if tok != ' ']) * 99.
            return [(confidence, parse.astimezone(self.timezone))]
        except ValueError:
            return []
