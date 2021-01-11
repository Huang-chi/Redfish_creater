#include <stdio.h>

#include "speedup_performance.h"

int slow_calc(int x, int a, int b){
	return a * x +b;
}

char* send_char_data(char* str){
	char* new_str = NULL;
	new_str = str;
	return new_str;
}
