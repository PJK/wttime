# wttime - A fuzzy time parser

![Lint and test](https://github.com/PJK/wttime/workflows/Tests/badge.svg?branch=master)

**DISCLAIMER:** At this point, the code is a dirty initial sketch of what I want
 to build. Assume I have no idea what I'm doing.

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
$ wttime 1231312312
UTC:     2009-01-07 07:11:52 (+0000)
$ wttime 1231231233000000
UTC:     2009-01-06 08:40:33 (+0000)
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
