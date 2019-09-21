from wttime.strategy import TimestampStrategy


class Parser:
    strategies = [
        TimestampStrategy()
    ]

    def parse(self, timespec):
        print([strategy.parse(timespec) for strategy in self.strategies])