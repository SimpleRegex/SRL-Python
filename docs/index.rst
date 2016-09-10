.. SRL-Python documentation master file, created by
   sphinx-quickstart on Sat Sep 10 14:56:53 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to SRL-Python's documentation!
======================================

`SRL-Python` is `Simple Regex Language`_ library for Python.
`SRL-Python` is pure Python, and has no other dependencies.
`SRL-Python` supports for Python 2.7/3.3/3.4/3.5 and pypy.

.. _Simple Regex Language: https://simple-regex.com

Contents:

.. toctree::
   :maxdepth: 2

   api

Usage
=====

Here is a short example, to illustrate the flavor of :mod:`srl`::

    >>> from srl import SRL
    >>> srl = SRL('digit exactly 3 times')
    >>> srl.pattern
    '[0-9]{3}'
    >>> srl.findall('0 01 012 013')
    ['012', '013']

License
=======

MIT License

Copyright (c) 2016 Simple Regex Language

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

