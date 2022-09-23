#include <stdio.h>
#include <math.h>
#include <time.h>

void main() {

  struct timespec start, finish;
  double elapsed;

  clock_gettime(CLOCK_MONOTONIC, &start);

  double log2 = log10(2.0);
  double log123 = log10(1.23);
  double log124 = log10(1.24);

  unsigned long j1, j2;
  unsigned long k = 1;
  unsigned long c = 0;
  while (1) {
    j1 = (unsigned long) ((log123 + k) / log2);
    j2 = (unsigned long) ((log124 + k) / log2);
    if (j2 > j1) {
      c++;
      if (c == 678910) {
        printf("%lu\n", j2);
        break;
      }
    }
    k++;
  }

  clock_gettime(CLOCK_MONOTONIC, &finish);
  elapsed = (finish.tv_sec - start.tv_sec);
  elapsed += (finish.tv_nsec - start.tv_nsec) / 1000000000.0;
  printf("et %.3fs\n", elapsed);
}

/*
runs in 0.5s - 3x faster than python with numba.
*/