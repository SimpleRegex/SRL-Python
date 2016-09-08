 # -*- coding: utf-8 -*-

import re
from glob import glob
from srl.builder import Builder
from srl.srl import SRL

def test_simple_phone_number_format():
    regex = Builder().literally('+').digit().between(1, 3) \
            .literally(' ').number().between(3, 4) \
            .literally('-').digit().once_or_more() \
            .must_end().get()
    assert re.match(regex, '+49 123-45')
    assert re.match(regex, '+492 1235-45')
    assert not re.match(regex, '+49 123 45')
    assert not re.match(regex, '49 123-45')
    assert not re.match(regex, 'a+49 123-45')
    assert not re.match(regex, '+49 123-45b')

def test_simple_email_format():
    reg = Builder().any_of(
        lambda q: q.digit().letter().one_of('._%+-')
    ).once_or_more().literally('@').either_of(
        lambda q: q.digit().letter().one_of('.-')
    ).once_or_more().literally('.').letter().at_least(2) \
    .must_end().case_insensitive()
    regex = reg.get()

    assert reg.is_valid()
    assert reg.is_matching('super-He4vy.add+ress@top-Le.ve1.domains')
    assert not reg.is_matching('sample.example.com')
    assert re.match(regex, 'sample@example.com')
    assert re.match(regex, 'super-He4vy.add+ress@top-Le.ve1.domains', reg.flags)
    assert not re.match(regex, 'sample.example.com')
    assert not re.match(regex, 'missing@tld')
    assert not re.match(regex, 'hav ing@spac.es')
    assert not re.match(regex, 'no@pe.123')
    assert not re.match(regex, 'invalid@email.com123')

def test_capture_group():
    builder = Builder()
    query = builder.literally('colo').optional('u').literally('r').any_of(lambda q: q.literally(':') & (lambda q: q.literally(' is'))).whitespace().capture(lambda q: q.letter().once_or_more(), 'color').literally('.')
    assert query.get_matches('my favorite color: blue.') == ['blue']
    assert query.get_matches('my favorite colour is green.') == ['green']
    assert not query.get_matches('my favorite colour is green!')
    assert query.findall('my favorite colour is green. And my favorite color: yellow.') == ['green', 'yellow']

def test_replace():
    query = Builder().capture(lambda q: q.any_character().once_or_more()) \
            .whitespace().capture(lambda q: q.digit().once_or_more()) \
            .literally(', ').capture(lambda q: q.digit().once_or_more()) \
            .case_insensitive()
    assert query.replace(r'\1 1, \3', 'April 15, 2003') == 'April 1, 2003'

def test_filter():
    query = Builder().capture(lambda q: q.uppercase_letter())
    assert query.filter(r'A:\g<0>', 'a1AB') == ('a1A:AA:B', 2)

def test_replace_callback():
    query = Builder().capture(lambda q: q.any_character().once_or_more()) \
            .whitespace().capture(lambda q: q.digit().once_or_more()) \
            .literally(', ').capture(lambda q: q.digit().once_or_more()) \
            .case_insensitive()
    assert query.replace(lambda params: 'invoked', 'April 15, 2003') == 'invoked'

def test_laziness():
    regex = Builder().literally(',').twice().whitespace().optional().first_match()
    assert regex.split('sample,one,, two,,three') == ['sample,one', ' two', 'three']

def test_raw():
    assert Builder().literally('foo').raw('b[a-z]r').is_valid()

