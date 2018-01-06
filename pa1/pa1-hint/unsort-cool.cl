-- COOL: Reverse-sort the lines from standard input. 

Class Main -- Main is where the program starts
  inherits IO { -- inheriting from IO allows us to read and write strings

	main() : Object { -- this method is invoked when the program starts
             let 
                 l : List <- new Nil, -- the sorted list input lines
                 done : Bool <- false -- are we done reading lines? 
             in {
               while not done loop {
                 let s : String <- in_string () in 
                 if s = "" then (* if we are done reading lines
                                 * then s will be "" *) 
                   done <- true 
                 else 
                   l <- l.insert(s) -- insertion sort it into our list
                 fi ;
               } pool ; -- loop/pool deliniates a while loop body
               l.print_list () ; -- print out the result
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

	print_list() : Object { abort() };
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
} ;

Class Nil inherits List { -- Nil is an empty list 

	insert(s : String) : List { (new Cons).init(s,self) }; 

	print_list() : Object { true }; -- do nothing 

} ;
