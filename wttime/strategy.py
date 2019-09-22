from datetime import datetime
from abc import ABC, abstractmethod
from typing import Tuple, Optional, NewType
import pytz


class Strategy(ABC):
    @abstractmethod
    def parse(self, timespec: str) -> Optional[Tuple[float, datetime]]:
        pass


class TimestampStrategy(Strategy):
    def parse(self, timespec):
        try:
            return [1., datetime.fromtimestamp(int(timespec))]
        except ValueError:
            return None
