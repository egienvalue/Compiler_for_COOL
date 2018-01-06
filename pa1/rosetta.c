#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct string_list_cell {
	char *head;
	struct string_list_cell *tail;
}
int visit(const void *a)
