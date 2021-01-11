#include "so_test.h"
int main()
{
    test_a();
    test_b();
    test_c();
    int a = send_int_data(50);
    printf("### Data: %d\n",a);
	char* str = "Robert";
	printf("### Data: %s\n",str);
	char* new_str = NULL;
	new_str = send_char_data(str);
	printf("### Data: %s\n",new_str); 
    return 0;
}
