#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// creat bool type for c 
typedef enum { false, true } bool;

// string list
struct string_list_cell {
    char *head;
    struct string_list_cell *tail;
};

struct edge {
    char *left;
    char *right;
};

struct string_list_cell *p_visited_list = NULL;//permanent mark
struct string_list_cell *t_visited_list = NULL;//temporary mark
int cycle_flag = 0;// flag show the cycle in graph
int line_count = 0;// lines count
int line_set_count = 0;// vertices count
int edge_count = 0;// edges count 

// comparison funtion using in quick sort
// sort the vertices and edges alphabetically 
int reverse_comparison (const void *a_ptr, const void *b_ptr);
int reverse_comparison_edges (const void *a_ptr, const void *b_ptr);

// judge whether the string array contains a specifical string or not
bool contains(struct string_list_cell *string_array, char *string);
int dfs(char *current, struct edge *edgelist);

// function to append element to the end of linked list
struct string_list_cell* append(struct string_list_cell *string_array,
                                char *string);
// function print all the linked list
int print_list(struct string_list_cell *string_array);


int main(void) {
    struct string_list_cell *lines = NULL;
    struct string_list_cell *lines_set = NULL;
    struct string_list_cell *lines_copy = NULL;
    while(1) {
        char line_buffer[80];
        fgets(line_buffer, sizeof(line_buffer), stdin);

        if (feof(stdin)) break;
        {
            struct string_list_cell *new_cell = malloc(sizeof(*new_cell));
            new_cell->head = strdup(line_buffer);
            new_cell->tail = lines;
            lines= new_cell;
            line_count++;
			
			// read lines to vertices, and remove duplicates
			// make the vertices become a set
            if(!contains(lines_set, new_cell->head)) {
                struct string_list_cell *new_vertice = malloc(sizeof(*new_vertice));
                new_vertice->head = new_cell->head;
                new_vertice->tail = lines_set;
                lines_set = new_vertice;
                line_set_count++;

            }


        }

    }
    edge_count = line_count/2;
    {
        char **array;
        char **vertices;
        struct edge *edges;
        int i = 0;
        array = malloc(line_count * sizeof(*array));
        vertices = malloc(line_set_count * sizeof(*vertices));
        edges = malloc(edge_count * sizeof(*edges));
        lines_copy = lines;
        while (lines != NULL) {
            array[i] = lines->head;
            i++;
            lines = lines->tail;
        }

        for(i=0;i<edge_count;i++) {
            edges[i].left = lines_copy->head;
            lines_copy = lines_copy->tail;
            edges[i].right = lines_copy->head;
            lines_copy = lines_copy->tail;
        }
        for(i=0;i<line_set_count;i++) {
            vertices[i] = lines_set->head;
            lines_set = lines_set->tail;
        }

        qsort(array, line_count, sizeof(array[0]), reverse_comparison);
        qsort(vertices,line_set_count, sizeof(vertices[0]), reverse_comparison);
        qsort(edges,edge_count, sizeof(edges[0]), reverse_comparison_edges);

        for (i=line_set_count-1;i>=0;i--) {	
            	dfs(vertices[i],edges);
        }
        print_list(p_visited_list);

    }

    return 0;
}

int reverse_comparison(const void *a_ptr, const void *b_ptr) {

    char *a = * (char **) a_ptr;
    char *b = * (char **) b_ptr;
    return strcmp(a,b);

}

int reverse_comparison_edges(const void *a_ptr, const void *b_ptr) {

    char *a = ((struct edge *)a_ptr)->right;
    char *b = ((struct edge *)b_ptr)->right;
    return strcmp(a,b);
}

bool contains(struct string_list_cell *string_array, char *string) {
    if (string_array==NULL)
        return false;
    if (strcmp(string_array->head, string)==0)
        return true;
    return contains(string_array->tail, string);
}

struct string_list_cell* append(struct string_list_cell *string_array,
                                char *string) {
    struct string_list_cell *new_cell = malloc(sizeof(*new_cell));
    new_cell->head = string;
    new_cell->tail = string_array;
    string_array= new_cell;
    return string_array;
}

int print_list(struct string_list_cell *string_array){
    if (string_array==NULL)
        return 0;
	printf("%s", string_array->head);
    print_list(string_array->tail);
    //printf("%s", string_array->head);
    return 0;
}

int dfs(char *current, struct edge *edgelist) {
    int i=0;
    if (contains(p_visited_list, current))
        return 0;
    if (contains(t_visited_list, current)) {
        cycle_flag = 1;
		printf("cycle\n");
        exit(0);
		return 0;
    }
    t_visited_list = append(t_visited_list,current);// add temporary mark
    for (i=edge_count-1;i>=0;i--){
        if(strcmp(current, edgelist[i].left)==0)
            dfs(edgelist[i].right, edgelist);// search adjecent vertices
    }
    p_visited_list = append(p_visited_list,current);//add permanent mark
    return 0;
}


