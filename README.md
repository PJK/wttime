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

Disambiguate various time specifications: 
```sh
$ wttime -t UTC 1231231233 1231231233000 1231231233000000 
UTC:     2009-01-06 08:40:33 (+0000)
UTC:     2009-01-06 08:40:33 (+0000)
UTC:     2009-01-06 08:40:33 (+0000)

$ wttime -t UTC 90000000 20200102 2020-01-02 "Nov 15" "Tuesday 10pm"
UTC:     1972-11-07 16:00:00 (+0000)
UTC:     2020-01-02 00:00:00 (+0000)
UTC:     2020-01-02 00:00:00 (+0000)
UTC:     2020-11-15 00:00:00 (+0000)
UTC:     2020-05-26 22:00:00 (+0000)
```

Flexible output formatting:
```sh
$ wttime -l -r --remote-timezone 'America/Chicago' -f '%Y-%m-%d %H:%M' -umy 1231231233000000
UTC:     2009-01-06 08:40
Local:   2009-01-06 09:40
Remote:  2009-01-06 02:40
Seconds: 1231231233
Millis:  1231231233000
Micros:  1231231233000000

$ wttime -nx -ns -y 20200810
1597010400000000
```

Plays well with others:
```sh
$ date | wttime
UTC:     2020-05-24 20:46:40 (+0000)
```

### Help
```sh
wttime --help
```

### FAQ 

#### How is this better than [dateutil](https://dateutil.readthedocs.io/en/stable/parser.html#dateutil.parser.parse)?

wttime can also handle timestamps, disambiguate more formats, and be used in from the shell. It does
use dateutil under the hood.

#### What is the deal with 'remote timezone'?

It is (unfortunately) common that companies or systems operate globally in a default timezone that 
is not UTC. In those cases, using an extra timezone can be convenient.
 

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
rm -r dist
python setup.py sdist
twine upload dist/*
```


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
