// JAVASCRIPT: topological sort 

var readline = require('readline');

var rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false  
  // terminal=false prevents ReadLine from echoing our input back to us
});

var lines = new Array(); // we'll store all of the lines here
var edges = new Array();
var vertices = new Array();
var p_visited = new Array();// permanent mark
var t_visited = new Array();// temporary mark
rl.on('line', function(this_line) {
  // Every time there is a line available on stdin, this function will be
  // called. 
  lines.push(this_line); // add this line to what we've seen so far
}); 
rl.on('close', function() {
  // When we're finally out of input on stdin, this function will be
  // called.

	// Here we use the filter to remove duplicates in lines, there are two way 
	// to remove duplicates, but the autograder only support the next one
	// vertices = Array.from(new Set(lines));
	vertices = lines.filter(function(item, pos, self) {
		// only return element that occupy one position in the list
    	return self.indexOf(item) == pos;
	});
	vertices.sort();
	// creat edges from lines
	for (var i = 0; i < lines.length; i=i+2) {
		var edge = [lines[i],lines[i+1]];
		edges.push(edge);
		//process.stdout.write(edge+'\n');
	}
	// sort the edge list according to the second part of its elements 
	edges.sort(function(a,b) {
		var char_a = a[1][0];
		var char_b = b[1][0];
		return (char_a === char_b) ? 0 : (char_a < char_b) ? -1 : 1
	});
	vertices.forEach(function dfs(current) {
		// if permanently visited, return
		if (include(current, p_visited))
			return 0;
		// if temporarily visited, print cycle 
		if (include(current, t_visited)){
			process.stdout.write("cycle\n");
			process.exit();	
		}
		t_visited.push(current);
		edges.forEach(function(each_edge) {
			if(each_edge[0]===current){
				dfs(each_edge[1]);
			}	
		});
		p_visited.push(current);	
	});
	// print permanent mark in order
	p_visited.forEach(function(x) {
		process.stdout.write(x+'\n')	
	}); 
});

// because the autograder doesn't support the new features
// so I can only write a function to check is a list contain a specific string
function include(string, string_array) {
	var i = string_array.length;
	while(i--){	
		if (string_array[i]==string){
			return true;
		}
	
	}
	return false;
}
