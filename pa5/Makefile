all:pa5

pa5: golden reader.py cool_classes.py
	./cool.dms --type test.cl
	python main.py test.cl-type
	diff -w my_test.s test.s > diff.output; [ $$? -eq 1 ]
	
golden:
	./cool.dms --opt --x86 test.cl
	./cool.dms --asm test.cl

clean:
	rm *.cl-lex *.cl-ast *.cl-type
