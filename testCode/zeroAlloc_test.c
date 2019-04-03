#include <stdlib.h>

int main()
{
	char str[40];
	int x = fgets(str, 40, stdin);
	int * myP = malloc(x);


	char str2[40];
	int y = fgets(str2, 40, stdin);
	if(y <= 0)
	{
		y = 8;
	}
	int * myP_two = malloc(y);
	
	return 0;
}
