// JAVASCRIPT: Reserve-Sort the lines from standard input

// We'll use the NodeJS ReadLine library to simplify line-by-line
// reading from the stdin input stream. 

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
var p_visited = new Array();
var t_visited = new Array();
rl.on('line', function(this_line) {
  // Every time there is a line available on stdin, this function will be
  // called. 

  lines.push(this_line); // add this line to what we've seen so far
}); 
rl.on('close', function() {
  // When we're finally out of input on stdin, this function will be
  // called.

  // We'll sort the lines in reverse order. We could also sort normally and
  // then call lines.reverse(), but we wanted to demonstrate passing a
  // custom comparison function to sort().
	
	// Here we use the filter to remove duplicates in lines
	// vertices = Array.from(new Set(lines));
	vertices = lines.filter(function(item, pos, self) {
    	return self.indexOf(item) == pos;
	});
	vertices.sort();	
	// Now we just iterate over each element in 'lines' and print it out.
	for (var i = 0; i < lines.length; i=i+2) {
		var edge = [lines[i],lines[i+1]];
		edges.push(edge);
		//process.stdout.write(edge+'\n');
	}
	edges.sort(function(a,b) {
		var char_a = a[1][0];
		var char_b = b[1][0];
		return (char_a === char_b) ? 0 : (char_a < char_b) ? -1 : 1
	});
	vertices.forEach(function dfs(current) {
		if (include(current, p_visited))
			return 0;
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
	p_visited.forEach(function(x) {
		process.stdout.write(x+'\n')	
	}); 
});
function include(string, string_array) {
	var i = string_array.length;
	while(i--){	
		if (string_array[i]==string){
			return true;
		}
	
	}
	return false;
}
