-- For the good test case, I used a long cool program. However, it is now sufficient enough,
-- we added a few more test cases in the end to make the program covers broader range
class VarList inherits IO {
  isNil() : Bool { true };
  head()  : Variable { { abort(); new Variable; } };
  tail()  : VarList { { abort(); new VarList; } };
  add(x : Variable) : VarList { (new VarListNE).init(x, self) };
  print() : SELF_TYPE { out_string("\n") };
};

class VarListNE inherits VarList {
  x : Variable;
  rest : VarList;
  isNil() : Bool { false };
  head()  : Variable { x };
  tail()  : VarList { rest };
  init(y : Variable, r : VarList) : VarListNE { { x <- y; rest <- r; self; } };
  print() : SELF_TYPE { { x.print_self(); out_string(" ");
	                  rest.print(); self; } };
};

(*
 * A list of closures we need to build.  We need to number (well, name)
 * the closures uniquely.
 *)
class LambdaList {
  isNil() : Bool { true };
  headE() : VarList { { abort(); new VarList; } };
  headC() : Lambda { { abort(); new Lambda; } };
  headN() : Int { { abort(); 0; } };
  tail()  : LambdaList { { abort(); new LambdaList; } };
  add(e : VarList, x : Lambda, n : Int) : LambdaList {
    (new LambdaListNE).init(e, x, n, self)
  };
};

class LambdaListNE inherits LambdaList {
  lam : Lambda;
  num : Int;
  env : VarList;
  rest : LambdaList;
  isNil() : Bool { false };
  headE() : VarList { env };
  headC() : Lambda { lam };
  headN() : Int { num };
  tail()  : LambdaList { rest };
  init(e : VarList, l : Lambda, n : Int, r : LambdaList) : LambdaListNE {
    {
      env <- e;
      lam <- l;
      num <- n;
      rest <- r;
      self;
    }
  };
};

class LambdaListRef {
  nextNum : Int <- 0;
  l : LambdaList;
  isNil() : Bool { l.isNil() };
  headE() : VarList { l.headE() };
  headC() : Lambda { l.headC() };
  headN() : Int { l.headN() };
  reset() : SELF_TYPE {
    {
      nextNum <- 0;
      l <- new LambdaList;
      self;
    }
  };
  add(env : VarList, c : Lambda) : Int {
    {
      l <- l.add(env, c, nextNum);
      nextNum <- nextNum + 1;
      nextNum - 1;
    }
  };
  removeHead() : SELF_TYPE {
    {
      l <- l.tail();
      self;
    }
  };
};

(*
 * Lambda expressions
 *
 *)

-- A pure virtual class representing any expression
class Expr inherits IO {

  -- Print this lambda term
  print_self() : SELF_TYPE {
    {
      out_string("\nError: Expr is pure virtual; can't print self\n");
      abort();
      self;
    }
  };

  -- Do one step of (outermost) beta reduction to this term
  beta() : Expr {
    {
      out_string("\nError: Expr is pure virtual; can't beta-reduce\n");
      abort();
      self;
    }
  };

  -- Replace all occurrences of x by e
  substitute(x : Variable, e : Expr) : Expr {
    {
      out_string("\nError: Expr is pure virtual; can't substitute\n");
      abort();
      self;
    }
  };

  -- Generate Cool code to evaluate this expression
  gen_code(env : VarList, closures : LambdaListRef) : SELF_TYPE {
    {
      out_string("\nError: Expr is pure virtual; can't gen_code\n");
      abort();
      self;
    }
  };
};

(*
 * Variables
 *)
class Variable inherits Expr {
  name : String;

  init(n:String) : Variable {
    {
      name <- n;
      self;
    }
  };

  print_self() : SELF_TYPE {
    out_string(name)
  };

  beta() : Expr { self };
  
  substitute(x : Variable, e : Expr) : Expr {
    if x = self then e else self fi
  };

  gen_code(env : VarList, closures : LambdaListRef) : SELF_TYPE {
    let cur_env : VarList <- env in
      { while (if cur_env.isNil() then
	          false
	       else
	         not (cur_env.head() = self)
	       fi) loop
	  { out_string("get_parent().");
	    cur_env <- cur_env.tail();
          }
        pool;
        if cur_env.isNil() then
          { out_string("Error:  free occurrence of ");
            print_self();
            out_string("\n");
            abort();
            self;
          }
        else
          out_string("get_x()")
        fi;
      }
  };
};

(*
 * Functions
 *)
class Lambda inherits Expr {
  arg : Variable;
  body : Expr;

  init(a:Variable, b:Expr) : Lambda {
    {
      arg <- a;
      body <- b;
      self;
    }
  };

  print_self() : SELF_TYPE {
    {
      out_string("\\");
      arg.print_self();
      out_string(".");
      body.print_self();
      self;
    }
  };

  beta() : Expr { self };

  apply(actual : Expr) : Expr {
    body.substitute(arg, actual)
  };

  -- We allow variables to be reused
  substitute(x : Variable, e : Expr) : Expr {
    if x = arg then
      self
    else
      let new_body : Expr <- body.substitute(x, e),
	  new_lam : Lambda <- new Lambda in
	new_lam.init(arg, new_body)
    fi
  };

  gen_code(env : VarList, closures : LambdaListRef) : SELF_TYPE {
    {
      out_string("((new Closure");
      out_int(closures.add(env, self));
      out_string(").init(");
      if env.isNil() then
        out_string("new Closure))")
      else
	out_string("self))") fi;
      self;
    }
  };

  gen_closure_code(n : Int, env : VarList,
		   closures : LambdaListRef) : SELF_TYPE {
    {
      out_string("class Closure");
      out_int(n);
      out_string(" inherits Closure {\n");
      out_string("  apply(y : EvalObject) : EvalObject {\n");
      out_string("    { out_string(\"Applying closure ");
      out_int(n);
      out_string("\\n\");\n");
      out_string("      x <- y;\n");
      body.gen_code(env.add(arg), closures);
      out_string(";}};\n");
      out_string("};\n");
    }
  };
};

(*
 * Applications
 *)
class App inherits Expr {
  fun : Expr;
  arg : Expr;

  init(f : Expr, a : Expr) : App {
    {
      fun <- f;
      arg <- a;
      self;
    }
  };

  print_self() : SELF_TYPE {
    {
      out_string("((");
      fun.print_self();
      out_string(")@(");
      arg.print_self();
      out_string("))");
      self;
    }
  };

  beta() : Expr {
    case fun of
      l : Lambda => l.apply(arg);     -- Lazy evaluation
      e : Expr =>
	let new_fun : Expr <- fun.beta(),
	    new_app : App <- new App in
	  new_app.init(new_fun, arg);
    esac
  };

  substitute(x : Variable, e : Expr) : Expr {
    let new_fun : Expr <- fun.substitute(x, e),
        new_arg : Expr <- arg.substitute(x, e),
        new_app : App <- new App in
      new_app.init(new_fun, new_arg)
  };

  gen_code(env : VarList, closures : LambdaListRef) : SELF_TYPE {
    {
      out_string("(let x : EvalObject <- ");
      fun.gen_code(env, closures);
      out_string(",\n");
      out_string("     y : EvalObject <- ");
      arg.gen_code(env, closures);
      out_string(" in\n");
      out_string("  case x of\n");
      out_string("    c : Closure => c.apply(y);\n");
      out_string("    o : Object => { abort(); new EvalObject; };\n");
      out_string("  esac)");
    }
  };
};

(*
 * Term: A class for building up terms
 *
 *)

class Term inherits IO {
  (*
   * The basics
   *)
  var(x : String) : Variable {
    let v : Variable <- new Variable in
      v.init(x)
  };

  lam(x : Variable, e : Expr) : Lambda {
    let l : Lambda <- new Lambda in
      l.init(x, e)
  };

  app(e1 : Expr, e2 : Expr) : App {
    let a : App <- new App in
      a.init(e1, e2)
  };

  (*
   * Some useful terms
   *)
  i() : Expr {
    let x : Variable <- var("x") in
      lam(x,x)
  };

  k() : Expr {
    let x : Variable <- var("x"),
        y : Variable <- var("y") in
    lam(x,lam(y,x))
  };

  s() : Expr {
    let x : Variable <- var("x"),
        y : Variable <- var("y"),
        z : Variable <- var("z") in
      lam(x,lam(y,lam(z,app(app(x,z),app(y,z)))))
  };

};

(*
 *
 * The main method -- build up some lambda terms and try things out
 *
 *)

class Main inherits Term {
  -- Beta-reduce an expression, printing out the term at each step
  beta_reduce(e : Expr) : Expr {
    {
      out_string("beta-reduce: ");
      e.print_self();
      let done : Bool <- false,
          new_expr : Expr in
        {
	  while (not done) loop
	    {
	      new_expr <- e.beta();
	      if (new_expr = e) then
		done <- true
	      else
		{
		  e <- new_expr;
		  out_string(" =>\n");
		  e.print_self();
		}
	      fi;
	    }
          pool;
	  out_string("\n");
          e;
	};
    }
  };

  eval_class() : SELF_TYPE {
    {
      out_string("class EvalObject inherits IO {\n");
      out_string("  eval() : EvalObject { { abort(); self; } };\n");
      out_string("};\n");
    }
  };

  closure_class() : SELF_TYPE {
    {
      out_string("class Closure inherits EvalObject {\n");
      out_string("  parent : Closure;\n");
      out_string("  x : EvalObject;\n");
      out_string("  get_parent() : Closure { parent };\n");
      out_string("  get_x() : EvalObject { x };\n");
      out_string("  init(p : Closure) : Closure {{ parent <- p; self; }};\n");
      out_string("  apply(y : EvalObject) : EvalObject { { abort(); self; } };\n");
      out_string("};\n");
    }
  };

  gen_code(e : Expr) : SELF_TYPE {
    let cl : LambdaListRef <- (new LambdaListRef).reset() in
      {
	out_string("Generating code for ");
	e.print_self();
	out_string("\n------------------cut here------------------\n");
	out_string("(*Generated by lam.cl (Jeff Foster, March 2000)*)\n");
	eval_class();
	closure_class();
	out_string("class Main {\n");
	out_string("  main() : EvalObject {\n");
	e.gen_code(new VarList, cl);
	out_string("\n};\n};\n");
	while (not (cl.isNil())) loop
	  let e : VarList <- cl.headE(),
	      c : Lambda <- cl.headC(),
	      n : Int <- cl.headN() in
	    {
	      cl.removeHead();
	      c.gen_closure_code(n, e, cl);
	    }
	pool;
	out_string("\n------------------cut here------------------\n");
      }
  };

  main() : Int {
    {
      i().print_self();
      out_string("\n");
      k().print_self();
      out_string("\n");
      s().print_self();
      out_string("\n");
      beta_reduce(app(app(app(s(), k()), i()), i()));
      beta_reduce(app(app(k(),i()),i()));
      gen_code(app(i(), i()));
      gen_code(app(app(app(s(), k()), i()), i()));
      gen_code(app(app(app(app(app(app(app(app(i(), k()), s()), s()),
                                   k()), s()), i()), k()), i()));
      gen_code(app(app(i(), app(k(), s())), app(k(), app(s(), s()))));
      0;
    }
  };
};

--multi-overriden
Class A {
	a : Int;
	methodAA (x : Int) : Int {
		1
	};	
	methodA () : Int {
		1
	};

};

Class B Inherits A {
	b: Int;
	methodB () : Int{
		1
	};
};

Class C Inherits B {
	c : Int;
	methodA () : Int{
		1
	};
};
--multi-let
class Multilet inherits IO{
	a : Int <-1;
	b : Int <-2;
	c : Int <-3;
	maiin() : Object{{
		out_int(a);
		let a : Int <- 5 in
			out_int(a) ;
		let a : Int <- 10 in
			out_int(b);
		let a : Int <- 5 in
			let b : Int <- 6, c : Int <- 7 in
				out_int(a + b + c);
	}};
};
--attribute and method test case
class Makin inherits IO{
	a : Int <-1;
	b : Int <-2;
	c : Int <-3;
	d : SELF_TYPE;
	maikn() : Object{{
		out_int(a);
		let a : Int <- 5 in
			out_int(a) ;
		let a : Int <- 10 in
			out_int(b);
		let a : Int <- 5 in
			let b : Int <- 6, c : Int <- 7 in
				out_int(a + b + c);
	}};
	var(m : Makin) : Makin{{
		1;
		new Makin;
	}};
};


class Mmain inherits IO{
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
	object(s : Mmain, l: Int, q : String) : SELF_TYPE{{
		1;
		self;
	}};
};

class Am inherits Mmain {
	m : Int <- 1;
	mm : SELF_TYPE;
	out_int : Int;
	main() : Object {{
		1;
		self(1);
	}};
	out_int(m: Int) : SELF_TYPE {{
		1;
		new SELF_TYPE;
	}}; 
	self (m : Int) : Int {{
		self@Am.object(new SELF_TYPE, 1,"s");
		1;
	}};
	
};

Class Main_rosetta Inherits IO {

	edges : EdgeList;
	vertices : List;
	p_visited : List;-- permanent mark
	t_visited : List;-- temparory mark
	cycle_flag : Bool;

	-- print edge list for testing
	print_edgelist(l : EdgeList) : Object {
		if isvoid l then
			self
		else {
			out_string(l.a());
			out_string(" -- ");
			out_string(l.b());
			out_string("\n");
			print_edgelist(l.next());
		} fi

	};
	-- print in oder of a List
	print_list(l : List) : Object {
		if isvoid l then
			self
		else {
			out_string(l.a());
			out_string("\n");
			print_list(l.next());

		} fi

	};
	-- print in reverse oder of a List
	print_list_reverse(l : List) : Object {
		if isvoid l then
			self
		else {
			print_list_reverse(l.next());
			out_string(l.a());
			out_string("\n");
		--	print_list(l.next());

		} fi
	
	};

	-- juedge whether a list includes a string
	contains(l : List, a : String) : Bool {{
		if isvoid l then
			false
		else {
			if l.a() = a then
				true
			else
				contains(l.next(),a)
			fi;
		} fi ;

	}};

	dfs(current: String, edges : EdgeList) : Object {{
			if contains(p_visited, current) then
				self
			else {
				if contains(t_visited, current) then {
					cycle_flag <- true;
					self;
				} else {			
					t_visited <- (new List).init(current, t_visited);
					let edge_ptr : EdgeList<- edges in
					-- iterate all the edges
					-- take any edges start with current	
					while not(isvoid edge_ptr) loop {
						if edge_ptr.a() = current then
							dfs(edge_ptr.b(), edges)
						else
							self	
						fi;
						edge_ptr <- edge_ptr.next();
					} pool;
					p_visited <- (new List).init(current, p_visited); 

				} fi;
				
			} fi;
				
		}};
	
	main_rosetta() : Object {{
		--out_string("hello world\n"); 
		let reading : Bool <- true in
		let cycle_flag : Bool <- false in
		while reading loop {
			let a : String <- in_string() in
			let b : String <- in_string() in
			{
			if b = "" then
				reading <- false
			else {
				if contains(vertices,a) then
				self
				else {
					-- insert element to vertices alphabetically 
					-- using insert sort
					if isvoid vertices then
						vertices <- (new List).init(a, vertices)
					else
						vertices <- vertices.insert(a)
					fi;
				}
				fi;
				if contains(vertices,b) then
					self
				else
					vertices <- vertices.insert(b)
				fi;
				if isvoid edges then
					edges <- (new EdgeList).init(a,b,edges)
				else 
					edges <- edges.insert(a,b)
				fi;
			}
			fi;
			};
		} pool;
	--	print_list(vertices);
	--	out_string("\n");
	--	out_string("topolist is:");
	--	out_string("\n");
		let vertice_ptr : List <- vertices in
		while not (isvoid vertice_ptr) loop {
			dfs(vertice_ptr.a(), edges);
			vertice_ptr <- vertice_ptr.next();
		} pool;
		if cycle_flag = true then
			out_string("cycle\n")
		else
			print_list_reverse(p_visited)
		fi;
	--	out_string("\n");
	--	out_string("edges");
	--	out_string("\n");
	--	print_edgelist(edges);

	}};



} ;

Class List {
	
	a : String;
	next : List;
	init(newa : String, newnext : List) : List {{
		a <- newa;
		next <- newnext;
		self;

	}};
	-- insert element alphabetically
	insert(s : String) : List {
		if not (a <= s) then          -- sort in reverse order
			(new List).init(s,self)
		else
		{
			if isvoid next then {
				next <- (new List).init(s,next);
				self;
			}
			else
				(new List).init(a,next.insert(s))
			fi;
		}
		fi
	};
	a() : String { a };
	next() : List { next };

};

Class EdgeList {
	a : String;
	b : String;
	next : EdgeList;
	
	init(newa : String, newb : String, newnext: EdgeList) : EdgeList {{
		a <- newa;
		b <- newb;
		next <- newnext;
		self;
	}};
	-- insert edge alphabetically 
	insert(s1 : String, s2 : String) : EdgeList {
	if not (b <= s2) then    
		(new EdgeList).init(s1,s2,self)
	else
	{
		if isvoid next then {
			next <- (new EdgeList).init(s1,s2,next);
			self;
		}
		else
			(new EdgeList).init(a, b, next.insert(s1,s2))
		fi;
	}
	fi
	};
	a() : String { a };
	b() : String { b };
	next() : EdgeList { next };

};

