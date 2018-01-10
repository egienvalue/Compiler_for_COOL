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
	struct edge *next;
};

int reverse_comparison (const void *a_ptr, const void *b_ptr);

bool contains(struct string_list_cell *string_array, char *string);
//bool contains(char **string_array, char *string);
int main(void) {
	struct string_list_cell *lines = NULL;
	struct string_list_cell *lines_set = NULL;
	struct string_list_cell *lines_copy = NULL;
	
	int line_count = 0;
	int line_set_count = 0;
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

			if(!contains(lines_set, new_vertice->head)) {
				new_vertice->head = strup(line_buffer);
				new_vertice->tail = lines_set;
				lines_set = new_vertice;
				line_set_count++;
			
			}
			
		
		}

	}
	{
		char **array;
		char **vertices;
		struct edge *edges;
		int i = 0;
		array = malloc(line_count * sizeof(*array));
		vertices = malloc(line_set_count * sizeof(*vertices));
		edges = malloc(line_count * sizeof(*array));
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


		for (i=0;i<line_count;i++) {
			printf("%s", array[i]);
		}

	}
	
	return 0;



}

int reverse_comparison(const void *a_ptr, const void *b_ptr) {

	char *a = * (char **) a_ptr;
	char *b = * (char **) b_ptr;
	return strcmp(b,a);

}

bool contains(struct string_list_cell *string_array, char *string) {
	if (string_array==NULL)
		return false;
	else if (reverse_comparison(string_array->head, string)==0)
		return true;
	else 
		contains(string_array->tail, string);
}

