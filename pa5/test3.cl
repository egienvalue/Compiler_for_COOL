class Main inherits IO{
	a : Int <- self(12, 13)+ self(21,33);
	b : Int <- self(11, 444) * self(23, self(12,55));
	c : Int <- self(18, 82) / self(12, 33);
	e : Int <- let fffff : Int <- 6,b : Int <- 8 in
			1*1;
	g : Int <- a;
	gi : Int <- (new A).self(1,self(12,self(12, self(12, self(11, self(11,self(11,45)))))));
	h : IO;
	d : SELF_TYPE;
	zhuzeyuan: Bool <- 1 < 2;
	tyro: Bool <- 5 < 3 + 4;
	zhuxx : Bool <- "a" < "b";
	friend : Bool <- new Main <= new Object;
	zhangsj : Bool <- not not not not not not not not not not not not false;
	exciting : Int <- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~231415;	
	shiqingduo : Int <- ~5;
	k : Object <- case d of
	        c : IO => 1+1;
	        a : Int => 1;
	        o : Object => 1;
       esac;
	qqq: String <- "hello world";
	main() : Object{{
		let b : Int <- 10 , a : Int <- 6 in
			out_int(b) ;
		let a : Int <- 10 in
			out_int(b);
		let a : Int <- 5 in
			let b : Int <- 6, c : Int <- 7 in
				out_int(a + b + c);
		-- overflow:
		if (2147483647 + 2147483647 <= 1) then{
			out_string("overflow");
		} else
			out_string("no overflow")
		fi;
		out_int(a);
		out_int(b);
		out_int(c);
		out_int(e);
		out_int(gi);
		out_int(exciting);

	}};
	main2() : Object{{
		out_int(1);	
	}};

	
	var(m : Main, k : Int) : Main{{
		1;
		m;
		k;
		a;
		new SELF_TYPE;
		case d of
	        c : IO =>  new Int;
	        a : A =>  2;
	        o : Main => {
		     out_string("Oooops\n");
		     abort(); 0;
		    };
       esac;
	   out_string("call var 1 time");
	   new Main;
	}};
	
	self (var1 : Int, var2: Int) : Int {{
		out_string("call self 1 time");
		var1 - var2 * var2 /var1 *var2 / (var2 + 1111) /2147483647;
	}};
};

class A inherits Main {
	m : Object <- main();
	mm : SELF_TYPE;
	mmm : Int <- self(1,1);
	main() : Object {{
		1;
		self(1,1);
	}};
	out_int(m: Int) : SELF_TYPE {{
		1;
		new SELF_TYPE;
	}}; 
	self (m : Int, mmmm: Int) : Int {{
		(new SELF_TYPE)@A.var((new A).var((new A).var(new Main, 33), 22), new Int);
		m - mmmm * m /mmmm *m / (m + 1111) /2147483647;
	}};
	
};


