# PYTHON: Reverse-sort the lines from standard input
import sys                # bring in a standard library


def visit(task):
    global topo_list, p_marked, t_marked
    if task in p_marked:
        return 0
    if task in t_marked:
        print "cycle"
        exit(0)
    t_marked.append(task)
    alpha_list = []
    for (task1, task2) in edges:
        if task1 == task:
            alpha_list.append(task2)
    for x in sorted(alpha_list):
        visit(x)
    p_marked.append(task)
    topo_list.append(task)

topo_list = []
p_marked = []
t_marked = []
lines = sys.__stdin__.readlines()   # read every line from stdin into an array!
lines = [x.strip() for x in lines]
#for x in lines:
#    print "line is ->", x, "<-"

it = iter(lines)
edges = zip(it, it)

#for (a, b) in edges:
#    print "edges is", a, "--", b

tasks = set([a for (a, b) in edges] + [b for (a, b) in edges])
tasks = sorted(tasks)

#for x in tasks:
#    print "task is", x

for x in tasks:
    if x not in p_marked:
            visit(x)

for x in topo_list:
    print x
