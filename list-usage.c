#include <stdio.h>
#include "list.h"

int main() {
	list_t* list = InitList(5); // Initializes list with 1 item with value 5.
	add(list, 1);  // Adds 1
	add(list, 4);  // Adds 4
	add(list, 6);  // Adds 6
	add(list, 7);  // Adds 7
	add(list, 8);  // Adds 8
	add(list, 14); // Adds 14
	add(list, 71); // Adds 71
	rem(list);	   // Removes last item (71)
	add(list, 71); // Adds 71
	pop(&list);    // Removes first item (5)
	pop(&list);    // Removes first item (1)
	pop(&list);    // Removes first item (4)
	pop(&list);    // Removes first item (6)
	rem_index(&list, 1); // Removes 2nd item from list. (8)
	print_list(list); // Prints list details. (7, 14, 71)
	printf("index of 7: [%d].\n", val_index(list, 7));   // Prints index of 7. (0)
	printf("index of 14: [%d].\n", val_index(list, 14)); // Prints index of 14. (1)
	printf("index of 27: [%d].\n", val_index(list, 27)); // Prints index of 27. (-1, not in list)
}