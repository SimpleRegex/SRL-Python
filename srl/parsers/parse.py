# -*- coding: utf-8 -*-

from ..utils import lex
from ..utils import yacc

# List of token names.
tokens = (
    # Symbols
    'LEFT_PARENTHESIS',
    'RIGHT_PARENTHESIS',
    'NUMBER',
    'CHARACTER',
    'STRING',

    # Keywords
    'K_LITERALLY',
    'K_ONE',
    'K_OF',
    'K_LETTER',
    'K_FROM',
    'K_TO',
    'K_UPPERCASE',
    'K_ANY',
    'K_EITHER',
    'K_NO',
    'K_DIGIT',
    'K_ANYTHING',
    'K_NEW',
    'K_LINE',
    'K_WHITESPACE',
    'K_TAB',
    'K_RAW',
    'K_EXACTLY',
    'K_TIMES',
    'K_BETWEEN',
    'K_AND',
    'K_OPTIONAL',
    'K_ONCE',
    'K_TWICE',
    'K_NEVER',
    'K_OR',
    'K_MORE',
    'K_AT',
    'K_LEAST',
    'K_AS',
    'K_UNTIL',
    'K_CAPTURE',
    'K_IF',
    'K_FOLLOWED',
    'K_BY',
    'K_ALREADY',
    'K_HAD',
    'K_CASE',
    'K_INSENSITIVE',
    'K_MULTI',
    'K_ALL',
    'K_LAZY',
    'K_BEGIN',
    'K_STARTS',
    'K_WITH',
    'K_MUST',
    'K_END',
    'K_CHARACTER',
    'K_NOT',

)

# Regular expression rules for tokens
t_LEFT_PARENTHESIS = r'\('
t_RIGHT_PARENTHESIS = r'\)'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_STRING = r'\"([^\\\n]|(\\.))*?\"'
t_K_LITERALLY = r'literally'
t_K_ONE = r'one'
t_K_OF = r'of'
t_K_LETTER = r'letter'
t_K_FROM = r'from'
t_K_TO = r'to'
t_K_UPPERCASE = r'uppercase'
t_K_ANY = r'any'
t_K_EITHER = r'either'
t_K_NO = r'no'
t_K_DIGIT = r'digit'
t_K_ANYTHING = r'anything'
t_K_NEW = r'new'
t_K_LINE = r'line'
t_K_WHITESPACE = r'whitespace'
t_K_TAB = r'tab'
t_K_RAW = r'raw'
t_K_EXACTLY = r'exactly'
t_K_TIMES = r'times?'
t_K_BETWEEN = r'between'
t_K_AND = r'and'
t_K_OPTIONAL = r'optional'
t_K_ONCE = r'once'
t_K_TWICE = r'twice'
t_K_NEVER = r'never'
t_K_OR = r'or'
t_K_MORE = r'more'
t_K_AT = r'at'
t_K_LEAST = r'least'
t_K_AS = r'as'
t_K_UNTIL = r'until'
t_K_CAPTURE = r'capture'
t_K_IF = r'if'
t_K_FOLLOWED = r'followed'
t_K_BY = r'by'
t_K_ALREADY = r'already'
t_K_HAD = r'had'
t_K_CASE = r'case'
t_K_INSENSITIVE = r'insensitive'
t_K_MULTI = r'multi'
t_K_ALL = r'all'
t_K_LAZY = r'lazy'
t_K_BEGIN = r'begin'
t_K_STARTS = r'starts'
t_K_WITH = r'with'
t_K_MUST = r'must'
t_K_END = r'end'
t_K_CHARACTER = r'character'
t_K_NOT = r'not'

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' ,\t'

t_CHARACTER = r'.'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

def p_character_with_quantifier(p):
    '''character : character quantifier
    '''
    p[0] = []
    p[0] += p[1]
    p[0] += p[2]

def p_character_with_anchor(p):
    '''character : character anchor
                 | anchor character
                 | anchor anchor
                 | character flag
                 | character lookaround
                 | lookaround character
                 | character character
    '''
    p[0] = []
    p[0] += p[1]
    p[0] += p[2]

def p_character_with_quantfier_and_anchor(p):
    '''character : character quantifier anchor
    '''
    p[0] = []
    p[0] += p[1]
    p[0] += p[2]
    p[0] += p[3]

def p_character_literally(p):
    'character : K_LITERALLY STRING'
    p[0] = [('literally', (p[2][1:-1], ))]

def p_character_one_of(p):
    'character : K_ONE K_OF STRING'
    p[0] = [('one_of', (p[3][1:-1], ))]

def p_character_letter(p):
    '''character : K_LETTER
                 | K_LETTER K_FROM CHARACTER K_TO CHARACTER
    '''
    p[0] = []
    if len(p) == 6:
        char_from = p[3]
        char_to = p[5]
    else:
        char_from = 'a'
        char_to = 'z'
    p[0].append(('letter', (char_from, char_to, ), ))

def p_character_uppercase_letter(p):
    '''character : K_UPPERCASE K_LETTER
                 | K_UPPERCASE K_LETTER K_FROM CHARACTER K_TO CHARACTER
    '''
    p[0] = p[0] or []
    if len(p) == 7:
        char_from = p[4]
        char_to = p[6]
    else:
        char_from = 'A'
        char_to = 'Z'
    p[0].append(('letter', (char_from, char_to, ), ))

def p_character_any_character(p):
    'character : K_ANY K_CHARACTER'
    p[0] = [('any_character', ())]

def p_character_no_character(p):
    'character : K_NO K_CHARACTER'
    p[0] = [('no_character', ())]

def p_character_digit(p):
    '''character : K_DIGIT
                 | K_DIGIT K_FROM NUMBER K_TO NUMBER
    '''
    p[0] = p[0] or []
    if len(p) == 6:
        num_from = p[3]
        num_to= p[5]
    else:
        num_from = 0
        num_to = 9
    p[0].append(('digit', (num_from, num_to, ), ))

def p_character_anything(p):
    'character : K_ANYTHING'
    p[0] = [('anything', ())]

def p_character_new_line(p):
    'character : K_NEW K_LINE'
    p[0] = [('new_line', ())]

def p_character_whitespace(p):
    '''character : K_WHITESPACE
    '''
    p[0] = [('whitespace', ())]

def p_character_no_whitespace(p):
    'character : K_NO K_WHITESPACE'
    p[0] = [('no_whitespace', ())]

def p_character_tab(p):
    'character : K_TAB'
    p[0] = [('tab', ())]

def p_character_raw(p):
    'character : K_RAW STRING'
    p[0] = [('raw', (p[2][1:-1], ))]

def p_quantifier_exactly_x_times(p):
    'quantifier : K_EXACTLY NUMBER K_TIMES'
    p[0] = [('exactly', (p[2], ))]

def p_quantifier_once(p):
    'quantifier : K_ONCE'
    p[0] = [('once', ())]

def p_quantifier_twice(p):
    'quantifier : K_TWICE'
    p[0] = [('twice', ())]

def p_quantifier_between_x_and_y_times(p):
    '''quantifier : K_BETWEEN NUMBER K_AND NUMBER K_TIMES
                  | K_BETWEEN NUMBER K_AND NUMBER
    '''
    p[0] = [('between', (p[2], p[4], ))]

def p_quantifier_optional(p):
    'quantifier : K_OPTIONAL'
    p[0] = [('optional', ())]

def p_quantifier_once_or_more(p):
    'quantifier : K_ONCE K_OR K_MORE'
    p[0] = [('once_or_more', ())]

def p_quantifier_never_or_more(p):
    'quantifier : K_NEVER K_OR K_MORE'
    p[0] = [('never_or_more', ())]

def p_quantifier_at_least_x_times(p):
    'quantifier : K_AT K_LEAST NUMBER K_TIMES'
    p[0] = [('at_least', (p[3], ))]


def p_group_string(p):
    'group : STRING'
    p[0] = ('lambda', [('literally', (p[1][1:-1], ))])

def p_group_subquery(p):
    'group : LEFT_PARENTHESIS character RIGHT_PARENTHESIS'
    p[0] = ('lambda', p[2])

def p_character_capture(p):
    'character : K_CAPTURE group'
    p[0] = [('capture', (p[2], None))]

def p_character_capture_as(p):
    'character : K_CAPTURE group K_AS STRING'
    p[0] = [('capture', (p[2], p[4][1:-1]))]

def p_group_any_of(p):
    '''character : K_ANY K_OF group
                 | K_EITHER K_OF group
    '''
    p[0] = [('any_of', (p[3], ))]

def p_group_non_capture(p):
    'character : group'
    p[0] = [('non_capture', (p[1], ))]

def p_group_until(p):
    '''character : K_UNTIL group
    '''
    p[0] = [('until', (p[2], ))]

def p_flag_case_insensitive(p):
    '''flag : K_CASE K_INSENSITIVE
    '''
    p[0] = [('case_insensitive', ())]

def p_flag_multi_line(p):
    '''flag : K_MULTI K_LINE
    '''
    p[0] = [('multi_line', ())]

def p_flag_all_lazy(p):
    '''flag : K_ALL K_LAZY
    '''
    p[0] = [('all_lazy', ())]

def p_anchor_begin_with(p):
    '''anchor : K_BEGIN K_WITH
              | K_STARTS K_WITH
    '''
    p[0] = p[0] or []
    p[0].append(('begin_with', ()))
    if len(p) == 4:
        p[0] += p[3]

def p_anchor_must_end(p):
    '''anchor : K_MUST K_END
    '''
    p[0] = p[0] or []
    if len(p) == 4:
        p[0] += p[1]
    p[0].append(('must_end', ()))

def p_lookaround_if_followed_by(p):
    'lookaround : K_IF K_FOLLOWED K_BY group'
    p[0] = [('if_followed_by', (p[4], ))]

def p_lookaround_if_not_followed_by(p):
    'lookaround : K_IF K_NOT K_FOLLOWED K_BY group'
    p[0] = [('if_not_followed_by', (p[5], ))]

def p_lookaround_if_already_had(p):
    'lookaround : K_IF K_ALREADY K_HAD group'
    p[0] = [('if_already_had', (p[4], ))]

def p_lookaround_if_not_already_had(p):
    'lookaround : K_IF K_NOT K_ALREADY K_HAD group'
    p[0] = [('if_not_already_had', (p[5], ))]

class SRLSyntaxError(Exception):
    pass

def p_error(p):
    raise SRLSyntaxError(str(p))

parser = yacc.yacc(debug=False)

def parse(string):
    return parser.parse(string, lexer=lexer, tracking=False)
