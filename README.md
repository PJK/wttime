# wttime - A fuzzy time parser

Tired of figuring out what this timestamp means? Done with format strings?
Cannot be bothered to care about all the seconds, millis, and jiffies?

You don't have to! **wttime** is a fuzzy parser that can recover and
disambiguate virtually any time specification you can throw at it.

## Getting Started

### Installation

```sh
pip install wttime
```

### Examples

```sh
$ wttime 1231312312
UTC:     2009-01-07 07:11:52 (+0000)
```

### Help
```sh
wttime --help
```

## TODOs

- add CI
- make open source
- push to pypi
- add parsers for standard timestrings
- refactor main to pull out logic and test it
- add type annotations and start checking

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
