from datetime import datetime
from abc import ABC, abstractmethod
from typing import Tuple, Optional, NewType
import math


class Strategy(ABC):
    @abstractmethod
    def parse(self, timespec: str) -> Optional[Tuple[float, datetime]]:
        pass


class TimestampStrategy(Strategy):
    @abstractmethod
    def parse_timestamp(self, timestamp: float):
        pass

    def parse(self, timespec):
        try:
            return self.parse_timestamp(float(timespec))
        except ValueError:
            return None


class SecondsTimestampStrategy(TimestampStrategy):
    def parse_timestamp(self, timestamp: float):
        # Most second timestamps are integers
        return [
            1. if int(timestamp) == timestamp else .7,
            datetime.fromtimestamp(timestamp)
        ]


class MillisTimestampStrategy(TimestampStrategy):
    def parse_timestamp(self, timestamp: float):
        # Prefer timestamps, prefer multiples of 1000
        if int(timestamp) == timestamp:
            confidence = 1. if timestamp % 1e3 == 0 else .9
        else:
            confidence = .7

        return [confidence, datetime.fromtimestamp(timestamp / 1e3)]


class MicrosTimestampStrategy(TimestampStrategy):
    def parse_timestamp(self, timestamp: float):
        # Prefer timestamps, prefer multiples of 1000000
        if int(timestamp) == timestamp:
            confidence = 1. if timestamp % 1e6 == 0 else .9
        else:
            confidence = .7

        return [confidence, datetime.fromtimestamp(timestamp / 1e6)]
