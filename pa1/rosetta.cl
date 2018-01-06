-- COOL: Reverse-sort the lines from standard input. 

Class Main -- Main is where the program starts
  inherits IO { -- inheriting from IO allows us to read and write strings
    let t_visited : List <- new Nil, p_visited : List <- new Nil in
	main() : Object { -- this method is invoked when the program starts
             let 
                 edges : EdgeList <- new EdgeNil, -- the sorted list input lines
                 done : Bool <- false -- are we done reading lines?
				-- t_visited : List <- new Nil,
				 --p_visited : List <- new Nil
             in {
               while not done loop {
                 let s1 : String <- in_string () in
				 let s2 : String <- in_string () in
                 if s2 = "" then (* if we are done reading lines
                                 * then s will be "" *) 
                   done <- true 
                 else 
                   edges <- edges.cons(s1, s2) -- insertion sort it into our list
                 fi; 
               } pool ; -- loop/pool deliniates a while loop body
			   edges.dfs("A", edges, t_visited, p_visited);
			   p_visited.print_list();
               edges.print_list () ; -- print out the result
			}
	};
};


(* The List type is not built in to Cool, so we'll have to define it 
 * ourselves. Cool classes can appear in any order, so we can define
 * List here _after_ our reference to it in Main. *) 
Class List inherits IO { 
        (* We only need three methods: cons, insert and print_list. *) 
           
        (* cons appends returns a new list with 'hd' as the first
         * element and this list (self) as the rest of the list *) 
	cons(hd : String) : Cons { 
	  let new_cell : Cons <- new Cons in
		new_cell.init(hd,self)
	};

        (* You can think of List as an abstract interface that both
         * Cons and Nil (below) adhere to. Thus you're never supposed
         * to call insert() or print_list() on a List itself -- you're
         * supposed to build a Cons or Nil and do your work there. *) 
	insert(i : String) : List { self };
	is_empty() : Bool { false };	
	print_list() : Object { abort() };

	contains(x : String) : Bool { false };
} ;

Class Cons inherits List { -- a Cons cell is a non-empty list 
	xcar : String;          -- xcar is the contents of the list head 
	xcdr : List;            -- xcdr is the rest of the list

	init(hd : String, tl : List) : Cons {
	  {
	    xcar <- hd;
	    xcdr <- tl;
	    self;
	  }
	};
	 
	is_empty() : Bool { false };
        (* insert() does insertion sort (using a reverse comparison) *) 
	insert(s : String) : List {
		if not (s < xcar) then          -- sort in reverse order
			(new Cons).init(s,self)
		else
			(new Cons).init(xcar,xcdr.insert(s))
		fi
	};

	print_list() : Object {
		{
		     out_string(xcar);
		     out_string("\n");
		     xcdr.print_list();
		}
	};

	contains(x : String) : Bool {
		if x = xcar then {
			out_string("contain");
			out_string(x);
			out_string("\n");
			true;
		}
		else
			xcdr.contains(x)
		fi
	};
	
} ;

Class Nil inherits List { -- Nil is an empty list 
	insert(s : String) : List { (new Cons).init(s,self) }; 

	is_empty() : Bool { true };
	print_list() : Object { true }; -- do nothing 
	
	contains(x : String) : Bool { false }; 

} ;

Class EdgeList inherits IO { 
        (* We only need three methods: cons, insert and print_list. *) 
           
        (* cons appends returns a new list with 'hd' as the first
         * element and this list (self) as the rest of the list *) 
	cons(s1 : String, s2 : String) : EdgeCons { 
	  let new_cell : EdgeCons <- new EdgeCons in
		new_cell.init(s1, s2, self)
	};

        (* You can think of List as an abstract interface that both
         * Cons and Nil (below) adhere to. Thus you're never supposed
         * to call insert() or print_list() on a List itself -- you're
         * supposed to build a Cons or Nil and do your work there. *) 
	insert(s1 : String, s2 : String) : EdgeList { self };
	
	print_list() : Object { abort() };

	contains(x : String) : Bool { false };

	dfs(current : String, edges : EdgeList, t_visited : List,
		p_visited : List) : List { new List};
} ;

Class EdgeCons inherits EdgeList { -- a Cons cell is a non-empty list 
	xs1 : String;	-- element of tuple left part
	xs2 : String;	-- element of tuple right part
	xcdr : EdgeList;            -- xcdr is the rest of the list

	init(s1 : String, s2 : String, tl : EdgeList) : EdgeCons {
	  {
	    xs1 <- s1;
		xs2 <- s2;
	    xcdr <- tl;
	    self;
	  }
	};
	  

	print_list() : Object {
		{
			 out_string("<");
		     out_string(xs1);
			 out_string(",");
			 out_string(xs2);
			 out_string(">");
		     out_string("\n");
		     xcdr.print_list();
		}
	};

	dfs(current : String, edges : EdgeList, 
		t_visited : List, p_visited : List) : List {
		{
			if p_visited.contains(current) then
				new Nil
			else
				if t_visited.contains(current) then
					(new List).cons("cycle")
				else
				{
					t_visited <- t_visited.cons(current);
					let new_p_visited : List <- p_visited.cons(current) in
					if (current = xs1) then {
						let recursive_call_result : List <- 
							edges.dfs(xs2, edges, t_visited, p_visited) in
						if recursive_call_result.is_empty() then
							xcdr.dfs(current, edges, t_visited, p_visited)
						else
							recursive_call_result
						fi;
					}
					else 
					{
						p_visited <- new_p_visited; 
						xcdr.dfs(current, edges, t_visited, p_visited);
					}
					fi;
				}
				fi	
			fi;
			
			

		}

	};


	
} ;

Class EdgeNil inherits EdgeList { -- Nil is an empty list 
	dfs(current : String, edges : EdgeList, t_visited : List, 
		p_visited : List) : List {new Nil};

	print_list() : Object { true }; -- do nothing 
	
} ;
