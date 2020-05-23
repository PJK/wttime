# wttime - A fuzzy time parser

[![Lint and test](https://github.com/PJK/wttime/workflows/Tests/badge.svg?branch=master)](https://github.com/PJK/wttime/actions?query=workflow%3ATests)

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

Guessing the most likely meaning:
```sh
$ wttime -t 'America/Los_Angeles' 20200101
UTC:     2020-01-01 08:00:00 (+0000)
$ wttime 1231231233000000
UTC:     2009-01-06 08:40:33 (+0000)
$ wttime 1231231233000
UTC:     2009-01-06 08:40:33 (+0000)
$ wttime 'Tuesday 10pm'
UTC:     2020-05-26 20:00:00 (+0000)
```

Variety of output formats:
```sh
$ wttime -l -r --remote-timezone 'America/Chicago' -f '%Y-%m-%d %H:%M' -umy 1231231233000000
UTC:     2009-01-06 08:40
Local:   2009-01-06 09:40
Remote:  2009-01-06 02:40
Seconds: 1231231233
Millis:  1231231233000
Micros:  1231231233000000

$ wttime -nx 20200810 -ns -y
1597010400000000
```

### Help
```sh
wttime --help
```

## TODOs

- get more data about format frequency in the wild
- figure out how to get feedback

## Development

### Add pre-commit hooks:

```
ln -sf $(pwd)/misc/hooks/pre-commit .git/hooks
```

### Run tests

```
pytest
```

### Publish to PyPI

```
python setup.py sdist
twine upload dist/*
```


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
