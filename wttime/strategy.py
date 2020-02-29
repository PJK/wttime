from datetime import datetime
from abc import ABC, abstractmethod
from typing import Tuple, Optional
import math


class Strategy(ABC):
    """Parses a string into a datetime and assigns it a confidence level.

    TODO: This design is completely arbitrary and the first thing that came
          to my mind.
    Confidence level guidance:
    (-infty, 0]
        Bad parse (consider returning None)
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
    def parse(self, timespec: str) -> Optional[Tuple[float, datetime]]:
        pass


class TimestampStrategy(Strategy):
    @abstractmethod
    def parse_timestamp(self, timestamp: float):
        pass

    def parse(self, timespec):
        try:
            # TODO: Handle non-decimals etc.
            return self.parse_timestamp(float(timespec))
        except ValueError:
            return None


class SecondsTimestampStrategy(TimestampStrategy):
    def parse_timestamp(self, timestamp: float):
        # Most second timestamps are integers
        return [
            100. if int(timestamp) == timestamp else 70.,
            datetime.fromtimestamp(timestamp)
        ]


class MillisTimestampStrategy(TimestampStrategy):
    def parse_timestamp(self, timestamp: float):
        # Prefer integers, prefer multiples of 1000
        if int(timestamp) == timestamp:
            confidence = 100. if timestamp % 1e3 == 0 else 90.
        else:
            confidence = 70.

        return [confidence, datetime.fromtimestamp(timestamp / 1e3)]


class MicrosTimestampStrategy(TimestampStrategy):
    def parse_timestamp(self, timestamp: float):
        # Prefer integers, prefer multiples of 1000000
        if int(timestamp) == timestamp:
            confidence = 100. if timestamp % 1e6 == 0 else 90.
        else:
            confidence = 70.

        return [confidence, datetime.fromtimestamp(timestamp / 1e6)]
