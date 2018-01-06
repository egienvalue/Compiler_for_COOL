/* C: Reverse-sort the lines from standard input */
#include <stdio.h>      /* bring in some standard library stuff */
#include <stdlib.h>
#include <string.h>

/* C doesn't come with a built-in list data-type, so we'll have to 
 * define our own lists. */ 
struct string_list_cell {
  /* we now list the fields in each list structure */ 
  char * head;  /* each list will carry a single string */ 
  /* In C we use "char *" or "array of characters" or "pointer to
   * characters" for "string". */ 
  struct string_list_cell * tail; /* and a pointer to another list cell */
} ; 
/* That 'struct' definition just introduces a new type -- it's like a 
 * class definition in Java. */ 

int reverse_comparison(const void *a, const void *b); 
/* That's a forward declaration of our comparison function for sorting.
 * We'll give the body of it later; for now we're just telling the 
 * C compiler that it exists. */ 

int main() {    /* 'main' is where your program starts */ 

  /* We'll make a variable of our special list type. Later we'll use it
   * to hold all of the lines we read in. Right now we'll initialize it to
   * NULL, the special "nothing here yet" value. */ 
  struct string_list_cell * lines = NULL; 

  int line_count = 0; /* we'll track the number of lines we read */ 

  while (1) { /* loop and read all of the lines from stdin */ 

    /* C does not have automatic memory management, so we must plan out
     * where we will store the lines we read in. We'll make a local
     * variable that can hold 80 characters for now. This sort of
     * pre-determined buffer size limit is a big problem in practice; we'll
     * return to it when we talk about language security later. */
    char line_buffer[80]; 

    fgets(line_buffer, sizeof(line_buffer), stdin); 
    /* This gets a line from stdin (standard input) and puts it
     * into 'line_buffer'. At most sizeof(line_buffer) (which is 80) 
     * characters will be read in. */

    if (feof(stdin)) break; 
    /* If that read didn't work because we've read in everything already
     * and now we're done, break out of this loop. "break" will transfer
     * control to the end of this while loop (which otherwise lasts
     * forever). */

    /* let's allocate a new list cell to hold our line */ 
    { /* In standard C I need to introduce a new { block } in order to
       * introduce a new local variable. */
      struct string_list_cell * new_cell =
        malloc(sizeof(*new_cell)); 
      /* malloc stands for "memory allocate" -- we have to tell it how
       * much space we need. It returns a pointer to the newly-allocated
       * space. In C, "*x" means loosely "tell me what x points to". */ 

      /* In a real C program you'd want to check and make sure that the
       * memory allocation succeeded and that you didn't run out of memory.
       * We'll skip that. */
      
      new_cell -> head = strdup(line_buffer); 
      /* strdup() makes a duplicate (a copy) of a string and returns a
       * poitner to it. We can't just store our local 'line_buffer' 
       * in the list because it's a stack-allocated local variable and
       * we're going to overwrite it when we read in the next line. */

      /* In a real C program we'd have to worry about freeing the memory
       * allocated by strdup (and the memory from malloc!) ... let's ignore
       * that, too. */ 

      new_cell -> tail = lines; 
      lines = new_cell; 
      /* We have just prepended "new_cell" to the beginning of "lines". */

      /* In C the arrow -> means "follow a pointer to a structure and
       * access its field". */

      line_count++;     /* increment our counter */ 
    } 
  } 

  /* OK, now we have to reverse-sort the list. C does have built-in
   * sorting, but it is only for arrays. I don't want to write bubblesort
   * (or whatever) by hand on my new linked list, so I'll convert my list
   * to an array. */ 
  {
    char * * array; 
    /* In the same way that a "char *" is like a "character array" and thus
     * a "string", a "string *" or "char * *" is an array of strings. */

    int i = 0; /* we'll use this local variable to index our array */

    array = malloc(line_count * sizeof(*array));

    /* How much space do we need? Well, we have line_count lines and each
     * line needs sizeof(char *) bytes. */ 

    /* We will walk down our linked list and put the ith element into
     * the ith slot in our array. */ 
    while (lines != NULL) { /* while we're not at the end */ 
      array[i] = lines->head; 
      /* store the line from the list into the array */
      i++; 
      lines = lines->tail; 
    } 

    qsort(array, line_count, sizeof(array[0]), reverse_comparison); 
    /* qsort is the C standard library (quick-)sorting function. We have to
     * tell it the array to sort, how many elements there are (line_count),
     * how big each element is (each one is the same size as the 0th
     * element of array), and what our comparison function is. We haven't
     * defined our comparison function yet; we'll get to that in a bit. */

    /* Now that the array has been destructively sorted in place, we can 
     * iterate over it and print out the results. */
    for (i=0; i<line_count; i++) {
      printf("%s",array[i]); /* print the ith element to standard output */ 
    } 
  } 

  return 0; /* we're done! */
} 

/* Now it's time to define our comparison function */ 
int reverse_comparison(const void *a_ptr, const void *b_ptr) {
  /* The contract for C-style standard library sorting is that your
   * comparison function takes pointers to elements rather than elements
   * themselves. So we'll just dereference everything once: */ 
  char * a = * (char * *)a_ptr;
  char * b = * (char * *)b_ptr;
  /* Now we want to compare a and b. */ 
  return strcmp(b,a); 
  /* The C standard library comes with a string comparison function that
   * does just what we need. We'll reverse the order of the arguments,
   * though. */ 
} 
