#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef enum { false, true } bool;

struct string_list_cell {
	char *head;
	struct string_list_cell *tail;
};

struct edge {
	char *left;
	char *right;
};

struct string_list_cell *p_visited_list = NULL;
struct string_list_cell *t_visited_list = NULL;
int cycle_flag = 0;
int line_count = 0;
int line_set_count = 0;
int edge_count = 0;

int reverse_comparison (const void *a_ptr, const void *b_ptr);
int reverse_comparison_edges (const void *a_ptr, const void *b_ptr);
bool contains(struct string_list_cell *string_array, char *string);
int dfs(char *current, struct edge *edgelist);
struct string_list_cell* append(struct string_list_cell *string_array, 
							   char *string);
int print_list(struct string_list_cell *string_array);
//bool contains(char **string_array, char *string);
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
			struct string_list_cell *new_vertice = malloc(sizeof(*new_cell));
			new_cell->head = strdup(line_buffer);
			new_cell->tail = lines;
			lines= new_cell;
			line_count++;

			if(!contains(lines_set, new_cell->head)) {
				new_vertice->head = strdup(line_buffer);
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
		i=0;

		while (lines_copy != NULL) {
			edges[i].left = lines_copy->head;
			lines_copy = lines_copy->tail;
			edges[i].right = lines_copy->head;
			lines_copy = lines_copy->tail;
			i++;
		}

		i=0;
		while (lines_set != NULL) {
			vertices[i] = lines_set->head;
			i++;
			lines_set = lines_set->tail;
		}	

		qsort(array, line_count, sizeof(array[0]), reverse_comparison);
		qsort(vertices,line_set_count, sizeof(vertices[0]), reverse_comparison);
		qsort(edges,edge_count, sizeof(vertices[0])*2, reverse_comparison_edges);
		for (i=0;i<line_count;i++) {
			printf("%s", array[i]);
		}
		for (i=0;i<edge_count;i++) {
			printf("%s := %s", edges[i].left, edges[i].right);	
		}

		for (i=0;i<line_set_count;i++) {
			dfs(vertices[i],edges);	
		}

		print_list(p_visited_list);

	}
	
	return 0;
}

int reverse_comparison(const void *a_ptr, const void *b_ptr) {

	char *a = * (char **) a_ptr;
	char *b = * (char **) b_ptr;
	return strcmp(b,a);

}

int reverse_comparison_edges(const void *a_ptr, const void *b_ptr) {
	
	char *a = ((struct edge *)a_ptr)->right;
	char *b = ((struct edge *)b_ptr)->right;
	return strcmp(b,a);
}

bool contains(struct string_list_cell *string_array, char *string) {
	if (string_array==NULL)
		return false;
	else if (strcmp(string_array->head, string)==0)
		return true;
	else 
		contains(string_array->tail, string);
}
struct string_list_cell* append(struct string_list_cell *string_array, 
								char *string) {
	struct string_list_cell *new_cell = malloc(sizeof(*new_cell));
	new_cell->head = string;
	new_cell->tail = string_array;
	string_array= new_cell;
}
int print_list(struct string_list_cell *string_array){
	if (string_array==NULL)
		return 0;
	print_list(string_array->tail);
	printf("%s", string_array->head);

}
int dfs(char *current, struct edge *edgelist) {
	int i;
	if (contains(p_visited_list, current))
		return 0;
	if (contains(t_visited_list, current)) {
		cycle_flag = 1;
		return 0;
	}
	append(t_visited_list,current);
	for (i=0;i<edge_count;i++){
		if(strcmp(current, edgelist[i].right))
			dfs(edgelist[i].right, edgelist);
	}
	append(p_visited_list,current);
}

