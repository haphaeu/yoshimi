#include <stdio.h>
#include <limits.h>

int main(void) {
    long foo1=LONG_MAX;
    long foo2=9223372036854775807;
    printf("%li\n", foo1);
    printf("%li\n", foo2);
}


