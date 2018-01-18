# RUBY: topological sort
require 'set'
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
$t_visited = [ ]
$p_visited = [ ]
vertices = lines.to_set
vertices = vertices.sort do |a,b| a<=>b end
edge = Struct.new(:left, :right)	#  edge struct to store left and right node
edges = []
i=0

# creat edges from standard input
until i > lines.length-2 do
	temp = edge.new(lines.at(i),lines.at(i+1))
	i = i+2
	edges.push temp
end
# sort edges alphabetically according to the right node
edges = edges.sort do |a,b| a.right <=> b.right end

def dfs(current,edges)
	if $p_visited.include?(current)
		return 0;
	end	
	if $t_visited.include?(current)
		puts "cycle\n"
		exit
	end
	$t_visited.push current
	# iterate through all the edge which start with current
	edges.each do |one_edge|
		if one_edge.left == current
			dfs(one_edge.right,edges)
		end
	end
	$p_visited.push current
	return 0;
end
vertices.each do |one_vertice| dfs(one_vertice,edges) end
$p_visited.each do |x| puts x end

