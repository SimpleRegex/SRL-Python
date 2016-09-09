SRL-Python
==============

Python Implementation of `Simple Regex <https://simple-regex.com>`_.

.. image:: https://travis-ci.org/SimpleRegex/SRL-Python.svg?branch=master
  :target: https://travis-ci.org/SimpleRegex/SRL-Python

Installation
-----------------

You can download and install the latest version of this software from the Python package index (PyPI) as below::

    $ pip install srl
    ✨🍰✨

SRL-Python supports:

* Python 2.7
* Python 3.3
* Python 3.4
* Python 3.5
* Pypy

Usage
-----------------

Class `SRL` takes a Simple Regex Language string as input.
`SRL` instance shares exactly same API with `re.RegexObject <https://docs.python.org/2/library/re.html#regular-expression-objects>`_::

    >>> from srl import SRL
    >>> srl = SRL('digit exactly 3 times')
    >>> srl.pattern
    '[0-9]{3}'
    >>> matched = srl.search('123')
    >>> matched.group()
    '123'

See more usages in `Specification <https://github.com/SimpleRegex/SRL-Python/blob/master/specification.md>`_.

Test
-----------------

`SRL-Python` uses nose as test runner.::

    $ pip install nose
    $ nosetests -c ./nose.cfg

License
-----------------

SRL is published under the MIT license. See `LICENSE` for more information.

Contribution
-----------------

Like this project? Want to contribute? Awesome! Feel free to open some pull requests or just open an issue.

Authors
-----------------

Send a pull request and bug the maintainer until it gets merged and published. :) Make sure to add yourself below.

- Lin Ju <soasme@gmail.com>
