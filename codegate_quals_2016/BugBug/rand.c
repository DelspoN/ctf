#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
	puts(argv[1]);
	srand(atoi(argv[1]));
	printf("%d\n", rand()%45+1);
        printf("%d\n", rand()%45+1);
        printf("%d\n", rand()%45+1);
        printf("%d\n", rand()%45+1);
        printf("%d\n", rand()%45+1);
        printf("%d\n", rand()%45+1);
	
        printf("%d\n", rand()%45+1);
        printf("%d\n", rand()%45+1);
        printf("%d\n", rand()%45+1);
        printf("%d\n", rand()%45+1);
        printf("%d\n", rand()%45+1);
        printf("%d\n", rand()%45+1);
	return 0;
}
