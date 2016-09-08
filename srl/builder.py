# -*- coding: utf-8 -*-

import re
import copy

from ._compat import string_types
from .parsers.parse import parse

class LazyError(Exception): pass

class Builder(object):


    def __init__(self, regex=None, flags=0, group='%s'):
        self.regex = regex or []
        self.flags = flags or 0
        self.compiled = None
        self.group = group or '%s'
        self.greedy_mode = True

    def escape(self, string):
        return re.escape(string)

    def literally(self, char):
        char = char.replace(r'\"', '"')
        char = self.escape(char)
        self.regex.append(r'(?:%s)' % char)
        return self

    def digit(self, start='0', end='9'):
        self.regex.append(r'[%s-%s]' % (start, end))
        return self

    number = digit

    def letter(self, start='a', end='z'):
        self.regex.append(r'[%s-%s]' % (start, end))
        return self

    def no_character(self):
        self.regex.append(r'\W')
        return self

    def uppercase_letter(self, start='A', end='Z'):
        self.regex.append(r'[%s-%s]' % (start, end, ))
        return self

    def any_character(self):
        self.regex.append(r'\w')
        return self

    def anything(self):
        self.regex.append(r'.')
        return self

    def new_line(self):
        self.regex.append(r'\n')
        return self

    def whitespace(self):
        self.regex.append(r'\s')
        return self

    def no_whitespace(self):
        self.regex.append(r'\S')
        return self

    def tab(self):
        self.regex.append(r'\t')
        return self

    def raw(self, string):
        self.regex.append(string)
        return self

    def between(self, start, end):
        self.regex.append(r'{%d,%d}' % (start, end))
        return self

    def once_or_more(self):
        if self.greedy_mode:
            self.regex.append(r'+')
        else:
            self.regex.append(r'+?')
        return self

    def never_or_more(self):
        if self.greedy_mode:
            self.regex.append(r'*')
        else:
            self.regex.append(r'*?')
        return self

    def optional(self, char=''):
        if self.greedy_mode:
            self.regex.append(r'%s?' % char)
        else:
            self.regex.append(r'%s??' % char)
        return self

    def first_match(self):
        if self.get()[-1] not in '+*}?':
            if self.regex[-1][-1] == ')' and self.get()[-2] in '+*}?':
                self.regex.append(self.revert_last()[0:-1] + '?)')
                return self
            raise LazyError('Cannot apply laziness at this point. Only applicable after quantifiers.')
        else:
            self.regex.append(r'?')
            return self

    lazy = first_match

    def exactly(self, count):
        self.regex.append(r'{%d}' % count)
        return self

    def once(self):
        return self.exactly(1)

    def twice(self):
        return self.exactly(2)

    def at_least(self, number):
        self.regex.append(r'{%d,}' % number)
        return self

    def add_closure(self, builder, conditions, exploder=''):
        builder.greedy_mode = self.greedy_mode
        if isinstance(conditions, string_types):
            subquery = builder.literally(conditions)
        elif callable(conditions):
            subquery = conditions(builder)
        elif isinstance(conditions, tuple) and conditions[0] == 'lambda' and isinstance(conditions[1], list):
            def callable_conditions(q):
                for method, arg in conditions[1]:
                    q = getattr(q, method)(*arg)
                return q
            subquery = callable_conditions(builder)
        else:
            subquery = builder.raw(conditions.get())

        self.regex.append(subquery.get(exploder))
        return self

    def capture(self, conditions, name=None):
        builder = Builder()
        if name:
            builder.group = '(?P<%s>%%s)' % name
        else:
            builder.group = '(%s)'
        return self.add_closure(builder, conditions)

    def any_of(self, conditions):
        builder = Builder()
        builder.group = '(?:%s)'
        return self.add_closure(builder, conditions, r'|')

    either_of = any_of

    def non_capture(self, conditions):
        builder = Builder()
        builder.group = '(?:%s)'
        return self.add_closure(builder, conditions)

    def until(self, conditions):
        try:
            self.lazy()
        except LazyError:
            pass
        builder = Builder()
        return self.add_closure(builder, conditions)

    def one_of(self, char):
        char = self.escape(char)
        self.regex.append(r'[%s]' % char)
        return self

    def if_followed_by(self, conditions):
        builder = Builder()
        builder.group = r'(?=%s)'
        return self.add_closure(builder, conditions)

    def if_not_followed_by(self, conditions):
        builder = Builder()
        builder.group = r'(?!%s)'
        return self.add_closure(builder, conditions)

    def if_already_had(self, conditions):
        builder = Builder()
        builder.group = r'(?<=%s)'
        previous_cond = self.revert_last()
        self.add_closure(builder, conditions)
        self.regex.append(previous_cond)
        return self

    def if_not_already_had(self, conditions):
        builder = Builder()
        builder.group = r'(?<!%s)'
        previous_cond = self.revert_last()
        self.add_closure(builder, conditions)
        self.regex.append(previous_cond)
        return self

    def begin_with(self):
        self.regex.append(r'^') # FIXME: assert
        return self

    starts_with = begin_with

    def must_end(self):
        self.regex.append(r'$')
        return self

    def case_insensitive(self):
        self.flags = self.flags | re.IGNORECASE
        return self

    def multi_line(self):
        self.flags = self.flags | re.MULTILINE
        return self

    def all_lazy(self):
        return self

    def revert_last(self):
        return self.regex.pop()

    def __and__(self, conditions):
        builder = Builder(group=self.group)
        return self.add_closure(builder, conditions)

    def get(self, implode=r''):
        return self.group % implode.join(self.regex)

    def compile(self):
        self.compiled = re.compile(self.get(), self.flags)
        return self

    def is_valid(self):
        try:
            self.compile()
            return True
        except re.error:
            return False

    def is_matching(self, string):
        if not self.compiled:
            self.compile()
        return bool(self.compiled.match(string, self.flags))

    def match(self, string):
        if not self.compiled:
            self.compile()
        return self.compiled.match(string, self.flags)

    def get_matches(self, string):
        if not self.compiled:
            self.compile()
        match = self.compiled.search(string)
        if match:
            return list(match.groups())

    def findall(self, string):
        if not self.compiled:
            self.compile()
        return self.compiled.findall(string, self.flags)

    def split(self, string):
        if not self.compiled:
            self.compile()
        return self.compiled.split(string, self.flags)

    def sub(self, repl, string):
        if not self.compiled:
            self.compile()
        return self.compiled.sub(repl, string, self.flags)

    replace = sub

    def subn(self, repl, string):
        if not self.compiled:
            self.compile()
        return self.compiled.subn(repl, string, self.flags)

    filter = subn

    @classmethod
    def parse(cls, string):
        builder = cls()
        parsed = parse(string)
        if not parsed:
            raise Exception('Invalid Simple Regex')

        for method, arg in parsed:
            if method == 'all_lazy':
                builder.greedy_mode = False

        for method, arg in parsed:
            builder = getattr(builder, method)(*arg)

        return builder.compile().compiled
