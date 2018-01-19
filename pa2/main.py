# Jun Luo
# lexer for cool language
import sys
import lex as lex

tokens = (
    'at',
    'colon',
    'comma',
    'divide',
    'dot',
    'equals',
    'identifier',
    'integer',
    'larrow',
    'lbrace',
    'le',
    'lparen',
    'lt',
    'minus',
    'plus',
    'rarrow',
    'rbrace',
    'rparen',
    'semi',
    'string',
    'tilde',
    'times',
    'type'
)

reserved = {
    'case' : 'case',
    'class' : 'class',
    'else' : 'else',
    'esac' : 'esac',
    'false' : 'false',
    'fi' : 'fi',
    'if' : 'if',
    'in' : 'in',
    'inherits' : 'inherits',
    'isvoid' : 'isvoid',
    'let' : 'let',
    'loop' : 'loop',
    'new' : 'new',
    'not' : 'not',
    'of' : 'of',
    'pool' : 'pool',
    'then' : 'then',
    'true' : 'true',
    'while' : 'while'
}

t_at = r'\@'
t_colon = r'\:'
t_comma = r'\,'
t_divide = r'/'
t_dot = r'\.'
t_equals = r'\='
t_identifier = r''
t_integer = r''
t_larrow = r'\<\-'
t_lbrace = r'\{'
t_le = r'\<\='
t_lparen = r'\('
t_lt = r'\<'
t_minus = r'\-'
t_plus = r'\+'
t_rarrow = r'\-\>'
t_rbrace = r'\}'
t_rparen = r'\)'
t_semi = r'\;'
t_string = r''
t_tilde = r'\~'
t_times = r'\*'
t_type = r'[A-Z]\w+'
