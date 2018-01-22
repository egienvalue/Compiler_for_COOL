# This is a lexer for cool (PA2)
# presented by Shiyu Wang (shiyuw)
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
    'COMENT',
    'type'
]

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
# Regular expression rules for simple tokens
t_at = r'\@'
t_colon = r'\:'
t_comma = r'\,'
t_divide = r'/'
t_dot = r'\.'
t_equals = r'\='
#t_identifier = r'' 
#t_integer = r''
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
#t_string = r''    TODO
t_tilde = r'\~'    
t_times = r'\*'
#t_type = r'SELF_TYPE' 

# regular expression for type

def t_type(t):
    r'[A-Z][a-zA-Z_0-9]*'
    temp = t.value.lower()
    if temp == "true" or temp == "false":
        return t
    t.type = reserved.get(temp, 'type')
    return t
 

# A regular expression rule with some action code
def t_integer(t):
        r'\d+'
        t.value = int(t.value)
	if t.value>=0 and t.value<=2147483647:
        	return t
	else:
		print("ERROR: %d : LEXER: Integer OutOfBound '%s'" % (t.lexer.lineno, t.value))
		exit(1)
		t.lexer.skip(1)

# identifiers

def t_identifier(t):
    r'[a-z][a-zA-Z_0-9]*'
    temp = t.value.lower()
    t.type = reserved.get(temp, 'identifier')
    return t

    
# Declare the state
states = (
  ('COMMENT','exclusive'),
  #('COMENT','exclusive'),
  ('string','exclusive')
)

# comments : comments need to be written in functions
def t_COMENT(t):
    r'--[^\n]*'
    return t
#def t_COMENT(t):
#    r'--'
#    t.lexer.code_start = t.lexer.lexpos        # Record the starting position
#    t.lexer.begin('COMENT')              # Enter 'COMENT' state
#def t_COMENT_newline(t):
#    r'\n'
#    t.value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos]
#    t.type = "COMENT"
#    t.lexer.lineno += t.value.count('\n')
#    t.lexer.begin('INITIAL')           
#    return t
#def t_COMENT_eof(t):
#    t.value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos]
#    t.type = "COMENT"
#    t.lexer.lineno += t.value.count('\n')
#    t.lexer.begin('INITIAL')           
#    return t
#
#def t_COMENT_error(t):
#    t.lexer.skip(1)
#
#t_COMENT_ignore = " \t\f\r\v"



# Match the first {. Enter ccode state.
def t_COMMENT(t):
    r'\(\*'
    t.lexer.code_start = t.lexer.lexpos        # Record the starting position
    t.lexer.level = 1                          # Initial brace level
    t.lexer.begin('COMMENT')                     # Enter 'ccode' state

# Rules for the ccode state
def t_COMMENT_lbrace(t):     
    r'\(\*'
    t.lexer.level +=1                

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
def t_COMMENT_eof(t):
    t.value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos]
    t.type = "COMMENT"
    t.lexer.lineno += t.value.count('\n')
    print("ERROR: %d: Lexer: EOF in (* comment *)" % (t.lexer.lineno))
    exit(1)
    t.lexer.skip(1)

# Ignored characters (whitespace)
t_COMMENT_ignore = " \t\f\r\v"

# skip bad chars
def t_COMMENT_error(t):
    t.lexer.skip(1)

# string : match a normal string
#def t_string(t):
#	r'\"([^\\\n]|(\\.)|[^\\0])*?\"'
#	return t		
def t_string(t):
    r'\"'
    t.lexer.code_start = t.lexer.lexpos        # Record the starting position
    t.lexer.level = 1
    t.lexer.begin('string')              # Enter 'ccode' state

def t_string_slashquote(t):
    r'\\(\\\\)*\"'
    t.lexer.begin('string')

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
            
    if len(t.value) > 1024:
        print("ERROR: %d: Lexer: string constant is too long (%d > 1024)" %
                (t.lexer.lineno,len(t.value)))
        exit(1)
        t.lexer.skip(1)
    t.type = "string"
    t.lexer.lineno += t.value.count('\n')
    t.lexer.begin('INITIAL')
    return t

def t_string_eof(t):
    print("ERROR: %d: LEXER: invalid character: \"" % (t.lexer.lineno))
    exit(1)
    t.lexer.skip(1)

def t_string_special(t):
    r'\n'
    print("ERROR: %d: LEXER: invalid character: \"" % (t.lexer.lineno))
    exit(1)
    t.lexer.skip(1)


def t_string_error(t):          # Special error handler for state 'bar'
    t.lexer.skip(1)

t_string_ignore = ' \t'

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
    if tok.type not in ['COMMENT','COMENT']:
        out_string = out_string + str(tok.lineno) + "\n"
        out_string = out_string + str(tok.type) + "\n"
    if tok.type in ['integer', 'identifier', 'string','type']:
	out_string = out_string + str(tok.value) + "\n"

# Write to file
outfile = open(sys.argv[1] + "-lex", 'w')
outfile.write(out_string)
outfile.close()

