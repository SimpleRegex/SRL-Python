 # -*- coding: utf-8 -*-

import re
from glob import glob
from srl.builder import Builder
from srl.srl import SRL

def test_simple_phone_number_format():
    regex = Builder().literally('+').digit().between(1, 3) \
            .literally(' ').number().between(3, 4) \
            .literally('-').digit().onceOrMore() \
            .mustEnd().get()
    assert re.match(regex, '+49 123-45')
    assert re.match(regex, '+492 1235-45')
    assert not re.match(regex, '+49 123 45')
    assert not re.match(regex, '49 123-45')
    assert not re.match(regex, 'a+49 123-45')
    assert not re.match(regex, '+49 123-45b')

def test_simple_email_format():
    reg = Builder().anyOf(
        lambda q: q.digit().letter().oneOf('._%+-')
    ).onceOrMore().literally('@').eitherOf(
        lambda q: q.digit().letter().oneOf('.-')
    ).onceOrMore().literally('.').letter().atLeast(2) \
    .mustEnd().caseInsensitive()
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
    query = builder.literally('colo').optional('u').literally('r').anyOf(lambda q: q.literally(':') & (lambda q: q.literally(' is'))).whitespace().capture(lambda q: q.letter().onceOrMore(), 'color').literally('.')
    assert query.getMatches('my favorite color: blue.') == ['blue']
    assert query.getMatches('my favorite colour is green.') == ['green']
    assert not query.getMatches('my favorite colour is green!')
    assert query.findall('my favorite colour is green. And my favorite color: yellow.') == ['green', 'yellow']

def test_replace():
    query = Builder().capture(lambda q: q.anyCharacter().onceOrMore()) \
            .whitespace().capture(lambda q: q.digit().onceOrMore()) \
            .literally(', ').capture(lambda q: q.digit().onceOrMore()) \
            .caseInsensitive()
    assert query.replace(r'\1 1, \3', 'April 15, 2003') == 'April 1, 2003'

def test_filter():
    query = Builder().capture(lambda q: q.uppercaseLetter())
    assert query.filter(r'A:\g<0>', 'a1AB') == ('a1A:AA:B', 2)

def test_replace_callback():
    query = Builder().capture(lambda q: q.anyCharacter().onceOrMore()) \
            .whitespace().capture(lambda q: q.digit().onceOrMore()) \
            .literally(', ').capture(lambda q: q.digit().onceOrMore()) \
            .caseInsensitive()
    assert query.replace(lambda params: 'invoked', 'April 15, 2003') == 'invoked'

def test_laziness():
    regex = Builder().literally(',').twice().whitespace().optional().firstMatch()
    assert regex.split('sample,one,, two,,three') == ['sample,one', ' two', 'three']

def test_raw():
    assert Builder().literally('foo').raw('b[a-z]r').is_valid()

def test_parse():
    assert SRL('literally "abc"').match('abc')
    assert SRL('one of "abc"').match('a')
    assert SRL('letter').match('a')
    assert SRL('letter from a to c').match('b')
    assert not SRL('letter from a to c').match('d')
    assert SRL('uppercase letter').match('A')
    assert SRL('letter from A to C').match('B')
    assert not SRL('letter from A to C').match('D')
    assert SRL('any character').match('a')
    assert SRL('no character').match(' ')
    assert SRL('digit').match('0')
    assert not SRL('anything').match('\n')
    assert SRL('anything').match('-')
    assert SRL('new line').match('\n')
    assert SRL('whitespace').match(' ')
    assert SRL('no whitespace').match('a')
    assert SRL('tab').match('\t')
    assert SRL('raw "[a-zA-Z]"').match('a')
    assert not SRL('raw "[a-z]"').match('A')
    assert SRL('digit exactly 2 times').match('00')
    assert SRL('digit exactly 2 times').match('000').group() == '00'
    assert not SRL('digit between 2 and 3 times').match('1')
    assert SRL('digit between 2 and 3 times').match('12')
    assert SRL('digit between 2 and 3').match('12')
    assert SRL('digit optional').match('a')
    assert not SRL('digit once or more').match('a')
    assert SRL('digit once or more').match('1')
    assert SRL('digit once or more').match('12')
    assert SRL('digit never or more').match('a')
    assert SRL('digit never or more').match('a1')
    assert not SRL('digit at least 2 times').match('1')
    assert SRL('digit at least 2 times').match('11')
    assert SRL('capture "abc"').match('abc')
    assert SRL('capture (digit once or more)').match('1').groups() == ('1', )
    assert SRL('capture (digit once or more) as "mydigit"').match('1').groups() == ('1', )
    assert SRL('any of (literally "sample")').match('sample')
    assert SRL('capture (anything once or more) until "m"').match('example')
    assert SRL('begin with must end').match('')
    assert SRL('letter case insensitive').match('A')
    assert SRL('capture (letter once or more) all lazy').match('a')

def test_rules():
    for filename in glob('tests/rules/*.rule'):
        with open(filename) as f:
            fdata = f.read()
            rule = SRL('literally "srl:", whitespace once or more, capture (anything once or more)')
            dsl = rule.compiled.search(fdata).groups()[0]
            srl = SRL(dsl)
            in_capture = False
            data = {'srl': None, 'matches': [], 'no_matches': [], 'captures': {}}
            for line in fdata.splitlines():
                if not line or line.startswith('#'):
                    continue
                if in_capture and not line.startswith('-'):
                    in_capture = False
                if line.startswith('srl: '):
                    data['srl'] = line[5:]
                elif line.startswith('match: "'):
                    data['matches'].append(line[8:-1])
                elif line.startswith('no match: "'):
                    data['no_matches'].append(line[11:-1])
                elif line.startswith('capture for "') and line.endswith('":'):
                    in_capture = line[13:-2]
                    data['captures'][in_capture] = {}
                elif in_capture and line.startswith('-'):
                    split = line[1:].split(': ')
                    data['captures'][in_capture][split[1].strip()] = split[2][1:-1]
