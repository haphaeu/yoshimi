/*fibmodule.c*/
 
#include <stdio.h>
 
int fib(int n)
{
    if (n < 2)
        return n;
    else
    {
        int f0=0; 
        int f1=1;
        int fb=0; 
        int i;
        for(i=1; i<n; i++)
        { 
            fb=f0+f1;
            f0=f1;
            f1=fb;
        }
        return fb;
    }
}
