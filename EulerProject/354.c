#include <stdio.h>
#include <math.h>

int main(void) {
    double Sqrt3 = pow(3,0.5);      /* constant */
    long verboseEvery=3000000; /* progess report*/

    long DistStart =   3;
    long DistEnd   =   21;
    long DistStep  =   1;

    long Distance = DistStart;
    long DistanceSqrd;
    long DistanceSqrd12;
    long firstLayer;
    long lastLayer;
    long layer;
    long layerSqrd;
    long ct;
    
    long delta;
    long i;
    
    float eps;
    float erro;
    double i_float;
    float p;
    
    eps=1.e-8;  /* define an error*/
   
    do { /*loop Distance*/
        DistanceSqrd   = Distance * Distance;
	DistanceSqrd12 = 12.0 * DistanceSqrd;
        firstLayer     = Distance/Sqrt3;
        lastLayer      = 2./3 * Distance;
        ct = 0;                            /* counter of hexs @ Distance*/
        layer=firstLayer;
        do { /*loop layer*/
            layerSqrd=layer*layer;
            delta   =DistanceSqrd12-27*layerSqrd;      /* Bhaskara*/
            i_float =(3.0*layer-pow(delta,0.5))/6.0;      /* only smaller root*/
            i=round(i_float);                    /* get closer integer*/
            erro=i-i_float;
	    if (erro<0) erro=-erro;
	    if (erro<eps & i>=0) {            /* check if i is close to an integer*/
                if (DistanceSqrd==3*(layerSqrd-layer*i+i*i)) { /*make sure i is integer*/
                    if (i==0) {
                        ct+=6;
		        /*printf("layer=%li, ct=%li\n", layer, ct); /**/
		    }
                    else if (!(layer&1) & i==layer>>1) { /* i==layer/2 and layer is even */
                        ct+=6;
		        /*printf("layer=%li, ct=%li\n", layer, ct); /**/
		    }
                    else {
                        ct+=12;
			/*printf("layer=%li, ct=%li\n", layer, ct); /**/
		    }
		}
	    }
            if (!(layer%verboseEvery)) {
                p=1.*(layer-firstLayer)/(lastLayer-firstLayer);
                printf("Found %li so far - %.2f%% done\r", ct, 100*p);
		fflush(stdout);
            }
            layer+=1;
        } while (layer <= lastLayer);
        printf("A total of %li hexagons found for a distance of %li\n", ct,  Distance);
        Distance += DistStep;
    } while (Distance < DistEnd);
    return 0;
}

