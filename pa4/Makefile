all:pa4

pa4:
	./cool.dms --parse test.cl
	python main.py test.cl-ast
golden:
	./cool.dms --parse test.cl

clean:
	rm *.cl-lex *.cl-ast
