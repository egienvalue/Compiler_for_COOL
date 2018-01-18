# PYTHON: topological sort
import sys                # bring in a standard library


def visit(vertice):
    global p_marked, t_marked
    if vertice in p_marked:
        return 0
    if vertice in t_marked:
        print "cycle"
        exit(0)
    t_marked.append(vertice)
    alpha_list = []
    for (left, right) in edges:
        if left == vertice:
            alpha_list.append(right)
    for x in sorted(alpha_list):
        visit(x)
    p_marked.append(vertice)


topo_list = []
p_marked = []   # permanent mark
t_marked = []   # temporary mark
lines = sys.__stdin__.readlines()   # read every line from stdin into an array!
lines = [x.strip() for x in lines]
it = iter(lines)
edges = zip(it, it)     # using zip to convert list to tuple list
vertices = set(lines)   # convert list to set
vertices = sorted(vertices)     # sorted alphabetically
for x in vertices:
    visit(x)
for x in p_marked:
    print x
