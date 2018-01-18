language: cool c pyton ruby javascript

For myself, I just can't get used to functional programming languages, so I
implement topological sort using the other five languages. Especially, I really
familiar with c and python. I will talk details in following paragraphs about 
the design. 

All my implementations use the algorithm from wikipedia:
 
	L ← Empty list that will contain the sorted nodes
	while there are unmarked nodes do
    select an unmarked node n
    visit(n) 

	function visit(node n)
		if n has a permanent mark then return
		if n has a temporary mark then stop (not a DAG)
		mark n temporarily
		for each node m with an edge from n to m do
	        visit(m)
	    mark n permanently
		add n to head of L


So we can just break the presudo code to diffent parts, and then I know what I
need to code next. I need to create following data structures and functions:

	1. data structure to store edges and vertices, typically, it is a list or
list of tuples(in my design I have used 2D string array, Linked list, or list of
tuples to store edges of the graph)
	2. function to sort edges and vertices alphabetically
	3. function to judge if a list contains a specific element 
	4. function to convert list into set
	5. using stack or list to store nodes we permanently visited and temporarily
visited( in my design, I used global variables to store the sequence of
permanently visited vertices. Actually, this sequence is what we want)
	6. function to read all the standard input string and store them
 
In terms of these features we need to implement, it doesn't exceed my
expectations that it is hardest to implement topological sort in c. I have to 
allocate memory manually and manipulate two-level pointers. it spends the 
longest time to debug comparing with implementations using orther languages
because the standard library in c doesn't have many features I can use to
simplify the implementation. For cool, things become a little bit better, not
using pointers, but finally there are 214 lines of code in .cl file. It is
reasonable becasue cool is designed for class. It can't support lots of
features we used in mordern language, so it become simpler for us to design a
compiler for cool.

For script languages, python, ruby, and javascript. They integrate lots of
useful data structure and functions we can use, such as using zip() function to
creat edge list of my graph, using set() to convert list into set. Finally, I
can use 30 lines of code to do the same thing comparing with c or cool.

The testcase is about how a person will dress up in the morning(generated from
the graph in Google Image). Then I combine
one of the testcase in the pa1-tesecase folder, century.list. So there are two independent
graph in my testcase for testing some corner cases. 

The answer for my own testcase is:

undershorts
pants
shirt
belt
tie
jacket
socks
shoes

