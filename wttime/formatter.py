import dateutil.tz as tz
from datetime import datetime, tzinfo


def format_parse(guess_confidence: float, guess: datetime, tzlocal: tzinfo,
                 confidence: bool, utc: bool, local: bool, remote: bool,
                 remote_timezone: tzinfo, format: str,
                 usec: bool, umilli: bool, umicro: bool,
                 label: bool) -> str:
    result = []
    dt_format = '{0: <8} {1}' if label else '{1}'
    if confidence:
        result.append('Confidence: %.10f' % guess_confidence)
    if utc:
        result.append(dt_format.format('UTC:', guess.astimezone(tz.UTC).strftime(format)))
    if local:
        result.append(dt_format.format('Local:', guess.astimezone(tzlocal).strftime(format)))
    if remote:
        result.append(
            dt_format.format('Remote:', guess.astimezone(remote_timezone).strftime(format)))
    if usec:
        result.append(dt_format.format('Seconds:', int(guess.timestamp())))
    if umilli:
        result.append(dt_format.format('Millis:', int(guess.timestamp() * 1e3)))
    if umicro:
        result.append(dt_format.format('Micros:', int(guess.timestamp() * 1e6)))
    return "\n".join(result)
