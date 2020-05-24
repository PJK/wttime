import dateutil.tz as tz
import sys
from datetime import datetime, tzinfo
from wttime.parser import Parser


class CLI:
    def __init__(self, parser: Parser, tzlocal: tzinfo,
                 confidence: bool, utc: bool, local: bool, remote: bool,
                 remote_timezone: tzinfo, format: str,
                 usec: bool, umilli: bool, umicro: bool,
                 label: bool):
        self.parser = parser
        self.tzlocal = tzlocal
        self.confidence = confidence
        self.utc, self.local, self.remote = utc, local, remote
        self.remote_timezone = remote_timezone
        self.format = format
        self.usec, self.umilli, self.umicro = usec, umilli, umicro
        self.label = label

    def format_parse(self, guess_confidence: float, guess: datetime) -> str:
        result = []
        dt_format = '{0: <8} {1}' if self.label else '{1}'
        if self.confidence:
            result.append('Confidence: %.10f' % guess_confidence)
        if self.utc:
            result.append(dt_format.format('UTC:', guess.astimezone(tz.UTC).strftime(self.format)))
        if self.local:
            result.append(dt_format.format('Local:',
                                           guess.astimezone(self.tzlocal).strftime(self.format)))
        if self.remote:
            result.append(dt_format.format('Remote:',
                                           guess.astimezone(self.remote_timezone).strftime(
                                               self.format)))
        if self.usec:
            result.append(dt_format.format('Seconds:', int(guess.timestamp())))
        if self.umilli:
            result.append(dt_format.format('Millis:', int(guess.timestamp() * 1e3)))
        if self.umicro:
            result.append(dt_format.format('Micros:', int(guess.timestamp() * 1e6)))
        return "\n".join(result)

    def parse(self, timespec: str) -> None:
        parse = self.parser.parse(timespec)
        if not parse:
            print("Couldn't parse the input. Please file a bug at "
                  "https://github.com/PJK/wttime/issues if I should have.")
            sys.exit(1)
        print(self.format_parse(*parse))
