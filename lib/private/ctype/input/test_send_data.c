#include <string.h>
#include <stdio.h>

#include "so_test.h"

int send_int_data(int value){
    value = 100;
    return value;
}

char* send_char_data(char* str){
	char* new_str = NULL;
	new_str = str;
	printf("### %s\n", new_str);
	return new_str;
}

