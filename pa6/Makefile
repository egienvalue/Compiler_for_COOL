all:pa6

pa6: golden reader.py cool_classes.py
	./cool.dms --type test.cl
	./cool.dms --opt --tac test.cl
	python main.py test.cl-type
	diff -w my_test.s test.s > diff.output; [ $$? -eq 1 ]
	
golden:
	./cool.dms --opt --x86 test.cl
	./cool.dms --asm test.cl

zip:
	zip submit.zip reader.py main.py cool_classes.py asm_classes.py num_temp.py methoddef.txt
	 
clean:
	rm *.cl-lex *.cl-ast *.cl-type
