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
  lines.sort(function(a,b) {
    return (b > a);
  }); 

  // Now we just iterate over each element in 'lines' and print it out.
  lines.forEach(function(sorted_line) {
    process.stdout.write(sorted_line + '\n'); 
  });
}); 
