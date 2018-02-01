# parser for pA3 for cool

import sys
from lex import LexToken
import yacc as yacc # the PLY parser

tokens_filename = sys.argv[1]
tokens_filehandle = open(tokens_filename, 'r')
tokens_lines = tokens_filehandle.readlines()
tokens_filehandle.close()

def get_token_line():
        global tokens_lines
        result = tokens_lines[0].strip()
        tokens_lines = tokens_lines[1:]
        return result

pa2_tokens = []

while tokens_lines != []:
    line_number = get_token_line()
    token_type = get_token_line()
    token_lexeme = token_type
    if token_type in ['identifier', 'integer', 'type']:
        token_lexeme = get_token_line()
    pa2_tokens = pa2_tokens + \
        [(line_number, token_type.upper(), token_lexeme)]

# use pA2 tokens as lexer
class PA2Lexer(object):
	def token(whatever):
		global pa2_tokens
		if pa2_tokens == []:
			return None
		(line, token_type, lexeme) = pa2_tokens[0]
		pa2_tokens = pa2_tokens[1:]
		tok = LexToken()
		tok.type = token_type
		tok.value = lexeme
		tok.lineno = line
		tok.lexpos = 0
		return tok

pa2lexer = PA2Lexer()

# Define our PA3 parser

tokens = (
	'PLUS',
	#'MINUS',
	'TIMES',
	'INTEGER',
	'CLASS',
	'IDENTIFIER',
	'TYPE',
	'COLON',
	'SEMI',
	'LBRACE',
	'RBRACE',
	'LARROW',
	#'RARROW'
	)

precedence = (
	('left' , 'PLUS'),
	('left', 'TIMES'),
	)

def p_program_classlist(p):
	'program : classlist'
	p[0] = p[1]

def p_classlist_none(p):
	'classlist : '
	p[0] = []

def p_classlist_some(p):
	'classlist : class SEMI classlist'
	p[0] = [p[1]] + p[3]

def p_class_noinherit(p):
	'class : CLASS type LBRACE featurelist RBRACE'
	p[0] = (p.lineno(1), 'class_noinherit', p[2], p[4] )

def p_type(p):
	'type : TYPE'
	p[0] = (p.lineno(1), p[1])

def p_identifier(p):
	'identifier : IDENTIFIER'
	p[0] = (p.lineno(1), p[1])

def p_featurelist_none(p):
	'featurelist : '
	p[0] =[]

def p_featurelist_some(p):
	'featurelist : feature SEMI featurelist'
	p[0] = [p[1]] + p[3]

def p_feature_attributenoinit(p):
	'feature : identifier COLON type'
	p[0] = (p.lineno(1), 'attribute_no_init', p[1], p[3])

def p_feature_attibuteinit(p):
	'feature : identifier COLON type LARROW exp'
	p[0] = (p.lineno(1), 'attribute_init', p[1] , p[3], p[5])

def p_exp_plus(p):
	'exp : exp PLUS exp'
	p[0] = ((p[1])[0], 'plus', p[1] , p[3])


#def p_exp_minus(p):
#	'exp : exp MINUS exp'
#	p[0] = (p.lineno(1), 'minus', p[1] , p[3])


def p_exp_times(p):
	'exp : exp TIMES exp'
	p[0] = ((p[1])[0], 'times', p[1] , p[3])

def p_exp_integer(p):
	'exp : INTEGER'
	p[0] = ((p[1])[0] , 'integer', p[1])

def p_error(p):
	if p:
		print "ERROR: ", p.lineno, ": Parser: parse error near ", p.type
		exit(1)
	else:
		print("ERROR: Syntax error at EOF")
# build PA3 parser
parser = yacc.yacc()
ast = parser.parse(lexer=pa2lexer)

#output PA3 CL-AST file
ast_filename = (sys.argv[1])[:-4] + "-ast"
fout = open(ast_filename, 'w')

def print_list(ast, print_element_function): # higher-order function
	fout.write(str(len(ast)) + "\n")
	for elem in ast:
		print_element_function(elem)

def print_identifier(ast):
	fout.write(str(ast[0]) + "\n")
	fout.write(ast[1] + "\n")

def print_exp(ast):
	fout.write(str(ast[0]) + "\n")
	if ast[1] in ['plus', 'times']:
		fout.write(ast[1] + "\n")
		print_exp(ast[2])
		print_exp(ast[3])
	elif ast[1] == 'integer':
		fout.write(ast[1] + "\n")
		fout.write(str(ast[2]) + "\n")
	else:
		print "unhandled expression"
		exit(1)

def print_feature(ast):
	if ast[1] == 'attribute_no_init':
		fout.write("attribute_no_init\n")
		print_identifier(ast[2])
		print_identifier(ast[3])
	elif ast[1] == 'attribute_init':
		fout.write("attribute_init\n")
		print_identifier(ast[2])
		print_identifier(ast[3])
		print_exp(ast[4])
	else:
		print "unhandled feature"
		exit(1)

def print_class(ast):
	print_identifier(ast[2])
	fout.write("no_inherits\n")
	print_list(ast[3], print_feature)

def print_program(ast):
	print_list(ast, print_class)

print_program(ast)

fout.close()
