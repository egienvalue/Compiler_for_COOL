all:pa5

pa5: golden reader.py cool_classes.py
	./cool.dms --type test.cl
	python main.py test.cl-type
golden:
	./cool.dms --x86 test.cl

clean:
	rm *.cl-lex *.cl-ast *.cl-type
