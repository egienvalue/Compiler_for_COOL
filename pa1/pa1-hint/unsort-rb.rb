# RUBY: Reverse-sort the lines from standard input
lines = [ ]     # a list variable to hold all the lines we'll read in
working = true  # are there still more lines to read in? 
while working
  line = gets           # read a line from standard input 
  if line == nil        # nil is "nothing, it didn't work" 
    working = false     # we're done reading stuff
  else
    lines[lines.length] = line # append 'line' to the end of 'lines
  end # end of 'if'
end # end of 'while' 
sorted = lines.sort do |a,b| # sort the list of lines
  # this do block is basically an anonymous function!  
  # |foo,bar| means "foo and bar are the arguments" 
  # we will tell it how to compare to arbitrary elements, a and b
  b <=> a       # <=> means "compare" -- we'll do it in reverse
end # end 'do' 
sorted.each do |one_line| # iterate over each element in the now-sorted list
  puts one_line           # write it to standard output
end # end 'do'
