class Main inherits IO{	
	d : Bool <- ~2147483647 = (0 - 2147483647);
	mm : Int <- if (~2147483647 + ~2147483647) <= 1 then
									1
				else
									1
				fi;		
	k : Object <- case d of
	        c : IO => 1;
	        a : Int => 1;
	        --o : Object => 1;
       esac;
	
	main() : Object{{
		let a : Int <- 5, b : Int <- 6, c : Int <- 7 in
				a + b;	
			--out_int(a+b);
	}};
};


