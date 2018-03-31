class Main inherits IO{	
	d : Int;
	k : Object <- case d of
	        c : IO => 1+1+1+1+1;
	        a : Int => case k of 
						s : IO => 1+1/2	;
						yuangao : String => let s : Int <- 1, sss : Int <- 2 in
												{sss;self;};
						esac;
	        --o : Object => 1;
       esac;
	
	main() : Object{{
		let a : Int <- 5, b : Int <- 6, c : Int <- 7 in
				a + b;	
			--out_int(a+b);
	}};
};


