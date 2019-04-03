#include <stdio.h>

int main()
{

	char * myBuf[80];
	fgets(myBuf, 80, stdin);
	sprintf("Hello There", myBuf)
	return 0;
}
