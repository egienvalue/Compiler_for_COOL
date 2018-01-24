# This is a lexer for cool (PA2)
# presented by Shiyu Wang (shiyuw) and Jun Luo (juluo)

import sys
import lex as lex

#list of token names
tokens = [
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
    'COMMENT',
    'LINE_COMMENT',
    'type'
]
#list of reserved token names
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

tokens = list(reserved.values()) + tokens
"""
Part 1. Simple regular expressions
In this part, all the simple tokens are expressed in a single line of regex
"""
t_at = r'\@'
t_colon = r'\:'
t_comma = r'\,'
t_divide = r'/'
t_dot = r'\.'
t_equals = r'\='
t_larrow = r'\<\-' 
t_lbrace = r'\{'   
t_le = r'\<\='     
t_lparen = r'\('
t_lt = r'\<'        
t_minus = r'\-'         
t_plus = r'\+'        
t_rarrow = r'\=\>'     
t_rbrace = r'\}'
t_rparen = r'\)'
t_semi = r'\;' 
t_tilde = r'\~'    
t_times = r'\*'

"""
Part 2. Function expressions
In this part, cases are little bit complex, so functions are needed to describe these tokens
Tokens in this part are: 'type', 'integer', 'identifier'
"""
# type
def t_type(t):
    r'[A-Z][a-zA-Z_0-9]*'
    temp = t.value.lower()
    if temp == "true" or temp == "false":
        return t
    t.type = reserved.get(temp, 'type')
    return t
# integer 
def t_integer(t):
        r'\d+'
        t.value = int(t.value)
	if t.value>=0 and t.value<=2147483647:
        	return t
	else:
		print("ERROR: %d : LEXER: Integer OutOfBound '%s'" % (t.lexer.lineno, t.value))
		exit(1)
		t.lexer.skip(1)
# identifier
def t_identifier(t):
    r'[a-z][a-zA-Z_0-9]*'
    temp = t.value.lower()
    t.type = reserved.get(temp, 'identifier')
    return t

# LINE_COMMENT is used to match single line comment(I must admit that the 'class name' is kind of wierd, but it is fine since the result is good).
def t_LINE_COMMENT(t):
    r'--[^\n]*'
    return t

"""
Part 3. State functions
In this part, some tokens are hard to express in one function, so we need to
declare them using relavant states. Tokens in this part are : 'COMMENT', 'string'
"""
# Declare the state
states = (
  ('COMMENT','exclusive'),
  ('string','exclusive')
)

# COMMENT is used to match multi-line comment
# Match the first {. Enter ccode state.
def t_COMMENT(t):
    r'\(\*'
    t.lexer.code_start = t.lexer.lexpos        # Record the starting position
    t.lexer.level = 1                          # Initial brace level
    t.lexer.begin('COMMENT')                     # Enter 'ccode' state
# lbrace to handle an event when there is a '('
def t_COMMENT_lbrace(t):     
    r'\(\*'
    t.lexer.level +=1                
# rbrace to handle an event when there is a ')'
def t_COMMENT_rbrace(t):
    r'\*\)'
    t.lexer.level -=1
    # If closing brace, return the code fragment
    if t.lexer.level == 0:
         t.value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos-2]
         t.type = "COMMENT"
         t.lexer.lineno += t.value.count('\n')
         t.lexer.begin('INITIAL')           
         return t
# eof, same as above
def t_COMMENT_eof(t):
    t.value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos]
    t.type = "COMMENT"
    t.lexer.lineno += t.value.count('\n')
    print("ERROR: %d: Lexer: EOF in (* comment *)" % (t.lexer.lineno))
    exit(1)
    t.lexer.skip(1)
# Ignored characters, same as above
t_COMMENT_ignore = " \t\f\r\v"
# skip bad chars
def t_COMMENT_error(t):
    t.lexer.skip(1)

# string : match a normal string
def t_string(t):
    r'\"'
    t.lexer.code_start = t.lexer.lexpos        # Record the starting position
    t.lexer.level = 1
    t.lexer.begin('string')              # Enter 'ccode' state
# when there are odd '\'s, the text continues to be valid
def t_string_slashquote(t):
    r'\\(\\\\)*\"'
    t.lexer.begin('string')
# when there are even '\'s, it will be an end of a string
def t_string_end(t):
    r'(\\\\)*\"'
    t.lexer.level -= 1
    t.value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos-1]
    for x in t.value:
        if ord(x)==0:
            print("ERROR: %d: LEXER: invalid character: \"" %
                    (t.lexer.lineno))
            exit(1)
            t.lexer.skip(1)
    # cool doesn't allow any string have more than 1024 characters        
    if len(t.value) > 1024:
        print("ERROR: %d: Lexer: string constant is too long (%d > 1024)" %
                (t.lexer.lineno,len(t.value)))
        exit(1)
        t.lexer.skip(1)
    t.type = "string"
    t.lexer.lineno += t.value.count('\n')
    t.lexer.begin('INITIAL')
    return t
# eof handling, same as above
def t_string_eof(t):
    print("ERROR: %d: LEXER: invalid character: \"" % (t.lexer.lineno))
    exit(1)
    t.lexer.skip(1)
# error message, can not complete lexing any more if encounters '\n'
def t_string_special(t):
    r'\n'
    print("ERROR: %d: LEXER: invalid character: \"" % (t.lexer.lineno))
    exit(1)
    t.lexer.skip(1)
# error message
def t_string_error(t):          
    t.lexer.skip(1)
# ignore characters
t_string_ignore = ' \t'

"""
Part 4 : other rules
In this part, we need to track line numbers, set ignore characters and define error handling rules for the main part
"""
# Define a rule so we can track line numbers
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \f\r\t\v'

# Error handling rule
def t_error(t):
	print("ERROR: %d: LEXER: Illegal character '%s'" % (t.lexer.lineno, t.value[0]))
	exit(1)
	t.lexer.skip(1)

"""
Part 5 : Main function
In this part, we complete the main function
"""
# Build the lexer
lexer = lex.lex()

# Run the lexer ...
file_name = sys.argv[1]
file_handle = open(file_name, "r")
file_contents = file_handle.read()
lexer.input(file_contents)

out_string = ""

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    # if token is a comment, skip it; otherwise print its line number and type
    if tok.type not in ['COMMENT','LINE_COMMENT']:
        out_string = out_string + str(tok.lineno) + "\n"
        out_string = out_string + str(tok.type) + "\n"
    # if token is an integer, an 'identifier', a 'string' or a 'type', we need to specify its value
    if tok.type in ['integer', 'identifier', 'string','type']:
	out_string = out_string + str(tok.value) + "\n"

# Write to file
outfile = open(sys.argv[1] + "-lex", 'w')
outfile.write(out_string)
outfile.close()

