#include<stdio.h>

int main()

{
   // POSITIVE_TESTS:
        void *bad_ptr = malloc(len + 8);
        memcpy(bad_ptr, spooky_buf, len + 7);

   // NEGATIVE_TESTS:
        void *other_bad_ptr = malloc(len + 1);
        memcpy(other_bad_ptr, spooky_buf, len);

     return 0;

}
