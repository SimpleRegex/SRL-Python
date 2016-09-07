# -*- coding: utf-8 -*-

import re
import copy

from .parsers.parse import parse

ESCAPE = re.compile(r'((P<special>[\[\\^$.|?*+()])|(P<nonspecial>.))')

class LazyError(Exception): pass

class Builder(object):


    def __init__(self, regex=None, flags=0, group='%s'):
        self.regex = regex or []
        self.flags = flags or 0
        self.compiled = None
        self.group = group or '%s'

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

    def noCharacter(self):
        self.regex.append(r'\W')
        return self

    def uppercaseLetter(self, start='A', end='Z'):
        self.regex.append(r'[%s-%s]' % (start, end, ))
        return self

    def anyCharacter(self):
        self.regex.append(r'\w')
        return self

    def anything(self):
        self.regex.append(r'.')
        return self

    def newLine(self):
        self.regex.append(r'\n')
        return self

    def whitespace(self):
        self.regex.append(r'\s')
        return self

    def noWhitespace(self):
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

    def onceOrMore(self):
        self.regex.append(r'+')
        return self

    def neverOrMore(self):
        self.regex.append(r'*')
        return self

    def optional(self, char=''):
        self.regex.append(r'%s?' % char)
        return self

    def firstMatch(self):
        if self.get()[-1] not in '+*}?':
            if self.regex[-1][-1] == ')' and self.get()[-2] in '+*}?':
                self.regex.append(self.revertLast()[0:-1] + '?)')
                return self
            raise LazyError('Cannot apply laziness at this point. Only applicable after quantifiers.')
        else:
            self.regex.append(r'?')
            return self

    lazy = firstMatch

    def exactly(self, count):
        self.regex.append(r'{%d}' % count)
        return self

    def once(self):
        return self.exactly(1)

    def twice(self):
        return self.exactly(2)

    def atLeast(self, number):
        self.regex.append(r'{%d,}' % number)
        return self

    def addClosure(self, builder, conditions, exploder=''):
        if isinstance(conditions, basestring):
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
        return self.addClosure(builder, conditions)

    def anyOf(self, conditions):
        builder = Builder()
        builder.group = '(?:%s)'
        return self.addClosure(builder, conditions, r'|')

    eitherOf = anyOf

    def nonCapture(self, conditions):
        builder = Builder()
        builder.group = '(?:%s)'
        return self.addClosure(builder, conditions)

    def until(self, conditions):
        try:
            self.lazy()
        except LazyError:
            pass
        builder = Builder()
        return self.addClosure(builder, conditions)

    def oneOf(self, char):
        char = self.escape(char)
        self.regex.append(r'[%s]' % char)
        return self

    def ifFollowedBy(self, conditions):
        builder = Builder()
        builder.group = r'(?=%s)'
        return self.addClosure(builder, conditions)

    def ifNotFollowedBy(self, conditions):
        builder = Builder()
        builder.group = r'(?!%s)'
        return self.addClosure(builder, conditions)

    def ifAlreadyHad(self, conditions):
        builder = Builder()
        builder.group = r'(?<=%s)'
        previous_cond = self.revertLast()
        self.addClosure(builder, conditions)
        self.regex.append(previous_cond)
        return self

    def ifNotAlreadyHad(self, conditions):
        builder = Builder()
        builder.group = r'(?<!%s)'
        previous_cond = self.revertLast()
        self.addClosure(builder, conditions)
        self.regex.append(previous_cond)
        return self

    def beginWith(self):
        self.regex.append(r'^') # FIXME: assert
        return self

    startWith = beginWith

    def mustEnd(self):
        self.regex.append(r'$')
        return self

    def caseInsensitive(self):
        self.flags = self.flags | re.IGNORECASE
        return self

    def multiLine(self):
        self.flags = self.flags | re.MULTILINE
        return self

    def allLazy(self):
        self.regex.append(r'?') # FIXME: assert
        return self

    def revertLast(self):
        return self.regex.pop()

    def __and__(self, conditions):
        builder = Builder(group=self.group)
        return self.addClosure(builder, conditions)

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

    def getMatches(self, string):
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
            builder = getattr(builder, method)(*arg)
        return builder.compile().compiled
