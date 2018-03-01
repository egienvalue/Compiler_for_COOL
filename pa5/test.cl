class Main inherits IO{
	a : Int <-1;
	b : Int <-2;
	c : Int <-3;
	d : SELF_TYPE;
	main() : Object{{
		out_int(a);
		let a : Int <- 5 in
			out_int(a) ;
		let a : Int <- 10 in
			out_int(b);
		let a : Int <- 5 in
			let b : Int <- 6, c : Int <- 7 in
				out_int(a + b + c);
	}};
	var(m : Main) : Main{{
		1;
		new SELF_TYPE;
		case d of
	        c : IO => a <- new Int;
	        a : A => b <- 2;
	        o : Main => {
		     out_string("Oooops\n");
		     abort(); 0;
		    };
       esac;
	   new Main;
	}};

};

class A inherits Main {
	m : Int <- 1;
	mm : SELF_TYPE;
	main() : Object {{
		1;
		self(1);
	}};
	out_int(m: Int) : SELF_TYPE {{
		1;
		new SELF_TYPE;
	}}; 
	self (m : Int) : Int {{
		(new SELF_TYPE)@A.var(new Main);
		1;
	}};
	
};


