/******************************************************************
 Implementation of the prime finding algorithm of

    ___ Sieve of Eratosthenes ___

 as per reference
 http://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
 
 A very fast algorithm. Instead of looking for primes,
 which involves modules and lots of divisions, it uses
 quick bit shifts to mark all non-primes numbers in a
 range - non-prime numbers are multiple of smaller numbers
 in this sequence.

 Optimisation is done by excluding all the even numbers,
 performing a number of 'seeks' of the magnitude os the
 half of the squared root of the upper bound of the sequence,
 and finally by strating each 'seek' at the square of its
 seed odd number.

 See wikipedia page for details.

 This was firstly written in Python, now translated to C
 for performance

 R. Rossi - July 2012
****************************************************************/

/* DEBUGGING
	Note that the code is marked with
		#ifdef DEBUG
		...
		#endif
	So, to debug the code, call the compiler with the 
	following option:
		gcc -DDEBUG meusPrimos.c
	This will tell the compiler to define a DEBUG directive,
	so that the debugging code will be executed.
	If this directive is not defined, the debugging code will
	be ignored and won't affect performance.
*/

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#define	PRIMEND		-999
#define	TRUE		1
#define FALSE		0
#define PRINTPRIMES	0
#define PRINT2FILE	1

int* primes(int n) {
	if(n<2) return NULL;
    
    //max number of primes up to 'n'
    //which is the number of odd numbers
    //discounting 1 (the prime number 2)
    int num=n/2+n%2-1;
	#ifdef DEBUG 
		printf("Numbers of prime to calculate: %d\n", num); 
	#endif
    //allocate an array filled with True
    //assumung initially that all numbers will be primes
    //this array represents all the odd numbers starting from 3
    //[3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,...,num]
    #ifdef DEBUG 
		printf("trying malloc\n");
	#endif
	short* pos=(short *) malloc( (num+1) * sizeof(short));
	if(pos==NULL) {
		printf("Error allocating memory.\n");
		return (int*)NULL;
	}
	#ifdef DEBUG 
		printf("malloc ok. filling array with TRUEs\n");
	#endif
	for(int i=0; i<num+1; i++) pos[i]=TRUE;
	#ifdef DEBUG 
		printf("array filled ok\n");
	#endif

    //number of factors to check is Sqrt(n)/2    
    int i_lim=(int)pow(n,0.5)>>1;
	#ifdef DEBUG
		printf("searching factors up to %d\n", i_lim);
	#endif
	//largest factor is the square root of the number
	//but in this case, as our array has only odd numbers, we need to do
	//only half the steps to get to the square root, so that's why the square
	//root is being devided by 2.
	int start; int step;
	#ifdef DEBUG
		printf("starting loop...\n");
	#endif
    for(int i=0; i<i_lim; i++) {
        if(!pos[i]) continue; //position already marked as False, skipping
		
        //
        //considering a sequence of the odd numbers starting at 3
        //[3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41...]
		// 0 1 2 3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 th
        //and also considering that the indexes of this sequence **start at 0**
        //the _start_ is the index in this sequence of the square of the i_th element
        //   i   i_th odd   odd^2  index
        //   0      3        9       3
        //   1      5       25      11
        //   2      7       49      23
        //   3      9       81      39
        //   ...
        // the _step_ will be the i_th element of the sequence
        //
        //the loop will work like this:
        // i=0 => start=3, step=3 => non-prime odds:[9,15,21,27,33,39,...]
        // i=1 => start=11,step=5 => non-prime odds:[25,35,45,55,65,...]
        // i=2 => start=23,step=7 => non-prime odds:[49,63,77,...]
        // ...
        start=(i*(i+3)<<1)+3;
        step=(i<<1)+3 ;
		#ifdef DEBUG
			printf("marking multiples of %d\r", (step<<1)+3);
			fflush(stdout);
		#endif
        for(int j=start; j<num; j+=step) 
            pos[j]=FALSE;
	}
	#ifdef DEBUG
		printf("loop done. allocating memory for primes\n");
	#endif
	//allocate memory for the array with primes
	int* primes = (int *) malloc (num * sizeof(int));
	if(primes==NULL) {
		printf("Error allocating memory.\n");
		return (int*)NULL;
	}
	#ifdef DEBUG
		printf("malloc ok. calculating primes...\n");
	#endif
    //need to consider 2!!!
	int idx=0;
    primes[idx]=2;
    //and now back calculates all the primes given their positions
    //if ith odd number is prime, ith_prime_number = 2*i + 3
	for(int i=0; i<num; i++)
		if(pos[i]) {
			idx++;
			primes[idx]= (i<<1)+3;
		}
	free(pos);
	primes[idx+1]=PRIMEND; //mark the end of the array
    return primes;
}

int main() {
	int max=2e6;
	time_t t_start, t_end;
	printf("Calculating primes up to %d\n", max);
	t_start=clock(); int *p = primes(max); t_end=clock();
	if(p==NULL) {
		printf("Error calculating primes.\n");
		return -1;
	}
	float t = (float)(t_end-t_start)/CLOCKS_PER_SEC;
	printf("Done. Run in %fs\n", t);
	if(PRINTPRIMES) {
		int i=0;
		while (p[i]!=PRIMEND) {
			printf("%d ", p[i]);
			i++;
		}
	}
	if(PRINT2FILE) {
		printf("Printing results to file.\n");
		FILE *pFile = fopen("meusPrimos.txt","w");
		if(pFile==NULL) { printf("Error in writting to file.\n"); return -1; }
		int i=0;
		while (p[i]!=PRIMEND) {
			fprintf(pFile, "\t%d", p[i]);
			if((i+1)%10==0) fprintf(pFile, "\n");
			i++;
		}
		
	}
	free(p);
	return 0;
}

