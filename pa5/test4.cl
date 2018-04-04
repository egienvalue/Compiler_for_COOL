Class A Inherits IO {
	a : Int;
	methodAA (x : Int) : SELF_TYPE {{
		out_int(x*x*x*x/222);
		self;
	}};	
	methodA (x : Int) : SELF_TYPE {{
		out_int(x*x*x*x);
		self;
	}};

};

Class B Inherits A {
	b: Int;
	methodB (x : Int) : SELF_TYPE{{
		out_int(x*x);
		self;
	}};
};

Class C Inherits B {
	c : Int;
	methodA (x : Int) : SELF_TYPE{{
		out_int(x*x*x);
		self;
	}};
};

Class Main Inherits IO{

	main() : Object {{
		(new C).methodA(23).methodA(87)@B.methodB(333).methodAA(123).methodAA(372).methodA(278);

	}};
};
