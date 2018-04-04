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
				let va1 : A, va2 : SELF_TYPE, va3 : Object <- self in
					let va1 : Main, va2 : SELF_TYPE, va3 : Object <- self in
						let va1 : Int, va2 : SELF_TYPE, va5 : Object <- self in
							let va1 : Bool, va2 : SELF_TYPE, va3 : Object <- self in
											{out_int(11111);
											 va2 <- self;
											 va1 <- true;
											 if var1 then
												out_string("right");	
											 else
												out_string("wrong");	
											 fi;
											};	
	}};	
	var(m : Main) : Main{{
		1;
		new SELF_TYPE;
		case d of
	        c : IO => a <- new Int;
	        a : A => out_string("type right");
	        o : Main => case d of
	        c : IO => a <- new Int;
	        a : A => out_string("type right");
	        o : Main => case d of
	        c : IO => a <- new Int;
	        a : A => b <- 2;
	        o : Main => {
		     out_string("Oooops\n");
		     abort(); 0;
		    };
       esac;
       esac; 
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


