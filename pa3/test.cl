Class Main Inherits IO {

	edges : EdgeList;
	vertices : List;
	p_visited : List;-- permanent mark
	t_visited : List;-- temparory mark
	cycle_flag : Bool;

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

	main() : Object {{
		--out_string("hello world\n"); 
	--	let reading : Bool <- true in
	--	let cycle_flag : Bool <- false in
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

};
