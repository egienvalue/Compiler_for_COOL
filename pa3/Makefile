all:pa3

pa3: golden
	./cool.dms --lex test.cl
	python main.py test.cl-lex
golden:
	./cool.dms --parse test.cl

clean:
	rm *.cl-lex *.cl-ast
