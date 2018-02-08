# parser for pA3 for cool
'''
Part 0. Read from file and get tokens
'''
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
    if token_type in ['identifier', 'integer', 'type', 'string']:
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
'''
Part 1. Define tokens and precedence. For the tokens, we can get directly from pA2, 
for precedence, check https://web.eecs.umich.edu/~weimerw/2015-4610/cool-manual/node40.html
'''
# Define our PA3 parser

tokens = (
	'PLUS',
	'MINUS',
	'TIMES',
	'DIVIDE',
	'INTEGER',
	'STRING',
	'CLASS',
	'IDENTIFIER',
	'TYPE',
	'COLON',
	'SEMI',
	'LBRACE',
	'RBRACE',
	'LARROW',
	'LT',
	'LE',
	'TILDE',
	'NOT',
	'EQUALS',
	'LPAREN',
	'RPAREN',
	'TRUE',
	'FALSE',
	'ISVOID',
	'AT',
	'DOT',
	'COMMA',
	'RARROW',
	'NEW',
	'OF',
	'IF',
	'FI',
	'ELSE',
	'LOOP',
	'POOL',
	'WHILE',
	'CASE',
	'ESAC',
	'INHERITS',
	'THEN',
	'LET',
	'IN',
	)

precedence = (
	('right', 'LARROW'),
	('right', 'NOT'),
	('nonassoc' , 'LE','LT','EQUALS'),
	('left' , 'PLUS', 'MINUS'),
	('left', 'DIVIDE', 'TIMES'),
	('right', 'ISVOID'),
	('right', 'TILDE'),
	('left', 'AT'),
	('left', 'DOT'),
)

'''
Part 2. Define matching rules, refer to the picture on https://web.eecs.umich.edu/~weimerw/2015-4610/cool-manual/node39.html
'''
# cool syntax matches the whole program
def p_program_classlist(p):
	'program : classlist'
	p[0] = p[1]

# cool syntax matches one or more classes in the program
def p_classlist_none(p):
	'classlist : '
	p[0] = []

def p_classlist_some(p):
	'classlist : class SEMI classlist'
	p[0] = [p[1]] + p[3]

def p_class_noinherit(p):
	'class : CLASS type LBRACE featurelist RBRACE'
	p[0] = (p.lineno(1), 'class_noinherit', p[2], p[4] )
def p_class_inherit(p):
	'class : CLASS type INHERITS type LBRACE featurelist RBRACE'
	p[0] = (p.lineno(1), 'class_inherit', p[2], p[4], p[6])

# cool syntax matches feature sentences
def p_featurelist_none(p):
	'featurelist : '
	p[0] =[]

def p_featurelist_some(p):
	'featurelist : feature SEMI featurelist'
	p[0] = [p[1]] + p[3]

def p_feature_attributenoinit(p):
	'feature : identifier COLON type'
	p[0] = ((p[1])[0], 'attribute_no_init', p[1], p[3])

def p_feature_attributeinit(p):
	'feature : identifier COLON type LARROW exp'
	p[0] = ((p[1])[0], 'attribute_init', p[1] , p[3], p[5])

def p_feature_method(p):
	'feature : identifier LPAREN formalarglist RPAREN COLON type LBRACE exp RBRACE'
	p[0] = ((p[1])[0], 'method', p[1], p[3], p[6], p[8])

# cool syntax matches formal, including formal list
def p_formalarglist_none(p):
	'formalarglist : '
	p[0] = []

def p_formalarglist_some(p):
	'formalarglist : formal moreformalarg'
	p[0] = [p[1]] + p[2]

def p_formalarglist_moreformalarg(p):	
	'moreformalarg : COMMA formal moreformalarg'
	p[0] = [p[2]] + p[3]

def p_formalarglist_nonemore(p):
	'moreformalarg : '
	p[0] = []

def p_formal(p):
        'formal : identifier COLON type'
        p[0] = (p.lineno(1), 'formal', p[1], p[3])

# cool syntax matches expression, this is the most complex one since there are lots of probabilities
def p_exp_assign(p):
        'exp : identifier LARROW exp'
        p[0] = ((p[1])[0], 'assign', p[1], p[3])

def p_exparglist_none(p):
        'exparglist : '
        p[0] = []
def p_exparglist_some(p):
        'exparglist : exp moreexparg'
        p[0] = [p[1]] + p[2]
def p_exparglist_moreexparg(p):
        'moreexparg : COMMA exp moreexparg'
        p[0] = [p[2]] + p[3]
def p_exparglist_nonemore(p):
        'moreexparg : '
        p[0] = []

def p_exp_staticdispatch(p):
        'exp : exp AT type DOT identifier LPAREN exparglist RPAREN'
        p[0] = ((p[1])[0], 'static_dispatch', p[1], p[3], p[5], p[7])

def p_exp_dynamicdispatch(p):
        'exp : exp DOT identifier LPAREN exparglist RPAREN'
        p[0] = ((p[1])[0], 'dynamic_dispatch', p[1], p[3], p[5])

def p_exp_self_dispatch(p):
        'exp : identifier LPAREN exparglist RPAREN'
        p[0] = ((p[1])[0], 'self_dispatch', p[1], p[3])

def p_exp_ifstatement(p):
        'exp : IF exp THEN exp ELSE exp FI'
        p[0] = (p.lineno(1), 'if',p[2], p[4],p[6])

def p_exp_whileloop(p):
        'exp : WHILE exp LOOP exp POOL'
        p[0] = (p.lineno(1), 'while', p[2], p[4])

def p_explist_none(p):
	'explist : '
	p[0] = []

def p_explist_some(p):
	'explist : exp SEMI explist'
	p[0] = [p[1]] + p[3]

def p_exp_block(p):
        'exp : LBRACE explist RBRACE'
        p[0] = (p.lineno(1), 'block', p[2])

def p_exp_let(p) :
        'exp : LET bindinglist IN exp'
        p[0] = (p.lineno(1), 'let', p[2], p[4])
def p_exp_case(p) :
        'exp : CASE exp OF caselist ESAC'
        p[0] = (p.lineno(1), 'case', p[2], p[4])

def p_exp_newtype(p):
        'exp : NEW type'
        p[0] = (p.lineno(1), 'new', p[2])

def p_exp_isvoid(p):
        'exp : ISVOID exp'
        p[0] = (p.lineno(1), 'isvoid', p[2])

def p_exp_plus(p):
	'exp : exp PLUS exp'
	p[0] = ((p[1])[0], 'plus', p[1] , p[3])

def p_exp_minus(p):
	'exp : exp MINUS exp'
	p[0] = ((p[1])[0], 'minus', p[1] , p[3])

def p_exp_times(p):
	'exp : exp TIMES exp'
	p[0] = ((p[1])[0], 'times', p[1] , p[3])

def p_exp_divide(p):
	'exp : exp DIVIDE exp'
	p[0] = ((p[1])[0], 'divide', p[1] , p[3])

def p_exp_tilde(p):
	'exp : TILDE exp'
	p[0] = (p.lineno(1), 'negate', p[2])

def p_exp_lt(p):
	'exp : exp LT exp'
	p[0] = ((p[1])[0], 'lt', p[1] , p[3])

def p_exp_le(p):
	'exp : exp LE exp'
	p[0] = ((p[1])[0], 'le', p[1] , p[3])

def p_exp_eq(p):
	'exp : exp EQUALS exp'
	p[0] = ((p[1])[0], 'eq', p[1] , p[3])

def p_exp_not(p):
	'exp : NOT exp'
	p[0] = (p.lineno(1), 'not', p[2])	

def p_exp_group(p):
	'exp : LPAREN exp RPAREN'
	p[0] = (p.lineno(1), 'group', p[2])		

def p_exp_integer(p):
	'exp : INTEGER'
	p[0] = (p.lineno(1) , 'integer', p[1])

def p_exp_string(p):
	'exp : STRING'
	p[0] = (p.lineno(1), 'string', p[1])

def p_exp_identifier(p):
	'exp : identifier'
	p[0] = ((p[1])[0], 'identifier', p[1])

def p_exp_true(p):
	'exp : TRUE'
	p[0] = (p.lineno(1), 'true')	

def p_exp_false(p):
	'exp : FALSE'
	p[0] = (p.lineno(1), 'false')

# cool syntax matches binding list, i.e. ID: type [<- exp], which is common in expressions
def p_bindinglist_some(p):
        'bindinglist : binding morebinding'
        p[0] = [p[1]] + p[2]

def p_bindinglist_moreformalarg(p):
        'morebinding : COMMA binding morebinding'
        p[0] = [p[2]] + p[3]

def p_bindinglist_nonemore(p):
        'morebinding : '
        p[0] = []

def p_bindinginit(p) :
        'binding : identifier COLON type LARROW exp'
        p[0] = ((p[1])[0], 'let_binding_init', p[1], p[3], p[5])

def p_bindingnoinit(p) :
        'binding : identifier COLON type'
        p[0] = ((p[1])[0], 'let_binding_no_init', p[1], p[3])

# cool syntax matches caselists, which is common in expressions
def p_caselist_some(p):
	'caselist : casearg SEMI morecasearg'
	p[0] = [p[1]] + p[3]
        
def p_caselist_more(p):
        'morecasearg : casearg SEMI morecasearg'
        p[0] = [p[1]] + p[3]

def p_caselist_nomore(p):
        'morecasearg : '
        p[0] = []

def p_casearg(p):
        'casearg : identifier COLON type RARROW exp'
        p[0] = ((p[1])[0], 'casearg', p[1],p[3],p[5])

# cool syntax matche type and identifier, which is common in expressions
def p_type(p):
	'type : TYPE'
	p[0] = (p.lineno(1), p[1])

def p_identifier(p):
	'identifier : IDENTIFIER'
	p[0] = (p.lineno(1), p[1])

# error catching rules
def p_error(p):
	if p:
		print "ERROR: ", p.lineno, ": Parser: parse error near ", p.type
		exit(1)
	else:
		print("ERROR: Syntax error at EOF")
# build PA3 parser
parser = yacc.yacc()
ast = parser.parse(lexer=pa2lexer)

'''
Part 3. Output
'''

#output PA3 CL-AST file
ast_filename = (sys.argv[1])[:-4] + "-ast"
fout = open(ast_filename, 'w')
# print_list used to print one or more arguments, print all arguments in the list using any print method.
def print_list(ast, print_element_function): # higher-order function 
        fout.write(str(len(ast)) + "\n")
        if len(ast) ==0:
            return
        for elem in ast:
		print_element_function(elem)
# print_identifier used to print identifiers
def print_identifier(ast):
	fout.write(str(ast[0]) + "\n")
	fout.write(ast[1] + "\n")
# print_exp used to print expressions
def print_exp(ast):
        if ast[1] in ['group'] :
            print_exp(ast[2])
            return
	fout.write(str(ast[0]) + "\n")
	if ast[1] in ['plus', 'times', 'minus', 'divide', 'le', 'lt','eq']:
		fout.write(ast[1] + "\n")
		print_exp(ast[2])
		print_exp(ast[3])
	elif ast[1] == 'integer':
                fout.write(ast[1] + "\n")
                fout.write(ast[2] + "\n")
        elif ast[1] == 'string':
                fout.write(ast[1] + "\n")
                fout.write(ast[2] + "\n")
        elif ast[1] in ['not', 'negate', 'isvoid']:
                fout.write(ast[1] + "\n")
                print_exp(ast[2])
        elif ast[1] in ['identifier'] :
                fout.write(ast[1] + "\n")
                print_identifier(ast[2])
        elif ast[1] in ['true', 'false']:
                fout.write(ast[1] + "\n")
        elif ast[1] in ['static_dispatch']:
                fout.write(ast[1] + "\n")
                print_exp(ast[2])
                print_identifier(ast[3])
                print_identifier(ast[4])
                print_list(ast[5], print_exp)
        elif ast[1] in ['dynamic_dispatch']:
                fout.write(ast[1] + "\n")
                print_exp(ast[2])
                print_identifier(ast[3])
                print_list(ast[4], print_exp)
        elif ast[1] in ['self_dispatch']:
                fout.write(ast[1] + "\n")
                print_identifier(ast[2])
                print_list(ast[3], print_exp)
        elif ast[1] in ['assign']:
                fout.write(ast[1] + "\n")
                print_identifier(ast[2])
                print_exp(ast[3])
        elif ast[1] in ['if'] :
                fout.write(ast[1] + "\n")
                print_exp(ast[2])
                print_exp(ast[3])
                print_exp(ast[4])
        elif ast[1] in ['while'] :
                fout.write(ast[1] + "\n")
                print_exp(ast[2])
                print_exp(ast[3])
        elif ast[1] in ['block'] :
                fout.write(ast[1] + "\n")
                print_list(ast[2], print_exp)
        elif ast[1] in ['new']:
                fout.write(ast[1] + "\n")
                print_identifier(ast[2])
        elif ast[1] in ['let'] :
                fout.write(ast[1] + "\n")
                print_list(ast[2], print_binding)
                print_exp(ast[3])
        elif ast[1] in ['case'] :
                fout.write(ast[1] + '\n')
                print_exp(ast[2])
                print_list(ast[3], print_casearg)
	else:
		print "unhandled expression"
		exit(1)
# print_casearg used to print case lists
def print_casearg(ast):
        if ast[1] == 'casearg' :
            print_identifier(ast[2])
            print_identifier(ast[3])
            print_exp(ast[4])
# print_binding used to print bindings
def print_binding(ast):
        if ast[1] == 'let_binding_init' :
            fout.write(ast[1] + "\n")
            print_identifier(ast[2])
            print_identifier(ast[3])
            print_exp(ast[4])
        elif ast[1] == 'let_binding_no_init' :
            fout.write(ast[1] + "\n")
            print_identifier(ast[2])
            print_identifier(ast[3])
# print_feature used to print features
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
	elif ast[1] == 'method':
           fout.write(ast[1] + "\n")
           print_identifier(ast[2])
           print_formallist(ast[3])
           print_identifier(ast[4])
           print_exp(ast[5])
	else:
	    print "unhandled feature"
	    exit(1)
# print_formalist used to print formal lists
def print_formallist(ast):
        print_list(ast, print_formal)
# print_formal used to print formals
def print_formal(ast):
        print_identifier(ast[2])
        print_identifier(ast[3])        
# print the one class
def print_class(ast):
        if ast[1] == 'class_noinherit' :
	    print_identifier(ast[2])
	    fout.write("no_inherits\n")
	    print_list(ast[3], print_feature)
        elif ast[1] == 'class_inherit' :
            print_identifier(ast[2])
            fout.write("inherits\n")
            print_identifier(ast[3])
            print_list(ast[4], print_feature)
# print the whole program
def print_program(ast):
	print_list(ast, print_class)
# call the print_program method, and it will call every detailed print functions automatically!
print_program(ast)

fout.close()
