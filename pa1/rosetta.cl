Class Main Inherits IO {

	edges : EdgeList;
	vertices : List;
	p_visited : List;
	t_visited : List;
	cycle_flag : Bool;
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
					-- iterate all the edges
					-- take any edges start with current				
					t_visited <- (new List).init(current, t_visited);
					let edge_ptr : EdgeList<- edges in
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
	
	main() : Object {{
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
				if isvoid vertices then
					vertices <- (new List).init(a, vertices)
				else
					vertices <- vertices.insert(a)
				fi;
			}
				--vertices <- (new List).init(a, vertices)
			fi;
			if contains(vertices,b) then
				self
			else
				vertices <- vertices.insert(b)
				--vertices <- (new List).init(b, vertices)
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

	insert(s1 : String, s2 : String) : EdgeList {
	if not (b <= s2) then          -- sort in reverse order
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
