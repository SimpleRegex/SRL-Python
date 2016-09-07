SRL.py
======

A Python Implementation of [Simple Regex](https://simple-regex.com/).

## How to install


    $ pip install srl

## How to use

    >>> from srl import SRL
    >>> regex_object = SRL('digit exactly 3 times')
    >>> matched = regex_object.search('123') # Exactly same API with class re.RegexObject
    >>> matched.group()
    '123'

## How to test

    $ pip install nose
    $ nosetests -c ./nose.cfg

## TODO

- [ ] Passed Simple Regex Specification
- [ ] Release 0.1.0
