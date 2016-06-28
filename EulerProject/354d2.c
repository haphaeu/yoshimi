#include <stdio.h>
#include <math.h>

/*
 * ok... this is too tough for me, I'm giving up... for the time being :)
 * 
 * need tohave a better look at this
 * http://eulersolutions.49.forumer.com/viewtopic.php?f=3&t=167
 * and this
 * http://www.math.kth.se/~kurlberg/eprints/marmon.pdf
 */


int main(void) {
    double Sqrt3 = pow(3,0.5);      /* constant */
    
    int veryVerbose=0; /*progress report by layer found*/
    int verboseEvery=0; /*progess report within layers*/
    int verboseDist=10; /*progress report within distances*/

    long DistSqrd_s    = 3;       /* seja d=n*sqrt(s) => d^2=n^2*s      */
    long DistSqrd_n    = 64151555;  /* logo (d_n+1)^2=(n+1)^2*s           */
                                  /* ou, (d_n+1)^2 = (d_n)^2 + (2n+1)*s */
                                  /* [tb pode-se fazer d^2=n^2*s^2 ...] */
    long DistSqrdStart = DistSqrd_n*DistSqrd_n*DistSqrd_s;
    long DistSqrdEnd   =   22346266026754075;

    long DistanceSqrd =DistSqrdStart;
    long DistanceSqrd12;
    long firstLayer;
    long lastLayer;
    long layer;
    long layerSqrd;
    long ct;
    long ctmax=0;
    long DstSqrdMax;
    
    long delta;
    long i;
    
    float eps;
    float erro;
    double i_float;
    float p;
    
    eps=1.e-8;  /* define an error*/
   
    do { /*loop Distance*/
        DistanceSqrd12 = 12 * DistanceSqrd;
        firstLayer     = pow(DistanceSqrd,0.5)/Sqrt3;
        lastLayer      = 2./3 * pow(DistanceSqrd,0.5);
        ct = 0;                            /* counter of hexs @ Distance*/
        layer=firstLayer;
        do { /*loop layer*/
            layerSqrd=layer*layer;
            delta   =DistanceSqrd12-27*layerSqrd;      /* Bhaskara*/
            i_float =(3.0*layer-pow(delta,0.5))/6.0;      /* only smaller root*/
            //printf("%f\n", i_float);
            i=round(i_float);                    /* get closer integer*/
            erro=i-i_float;
            if (erro<0) erro=-erro;
            if (erro<eps & i>=0) {            /* check if i is close to an integer*/
                if (DistanceSqrd==3*(layerSqrd-layer*i+i*i)) { /*make sure i is integer*/
                    if (i==0) {
                        ct+=6;
                        if (veryVerbose) printf("found 6 hexagons at layer=%li and i=%li, ct=%li\n", layer, i, ct);
                    }
                    else if (!(layer&1) & i==layer>>1) { /* i==layer/2 and layer is even */
                        ct+=6;
                        if (veryVerbose) printf("found 6 hexagons at layer=%li and i=%li, ct=%li\n", layer, i, ct);
                    }
                    else {
                        ct+=12;
                        if (veryVerbose) printf("found 12 hexagons at layer=%li and i=%li, ct=%li\n", layer, i, ct);
                    }
                }
            }
            if (verboseEvery) if (!(layer%verboseEvery)) {
                p=1.*(layer-firstLayer)/(lastLayer-firstLayer);
                printf("Found %li so far - %.2f%% done\r", ct, 100*p);
                fflush(stdout);
            }
            layer+=1;
        } while (layer <= lastLayer);
        if(ct>ctmax) {
          ctmax=ct;
          DstSqrdMax=DistanceSqrd;
        }
        if (ct==450) printf("!!! Fount %li hexagons found for a distance^2= %li !!!\n", ct,  DistanceSqrd);
        if (verboseDist) if (!((DistanceSqrd-DistSqrdStart)%verboseDist)) { 
            p=1.*(DistanceSqrd-DistSqrdStart)/(DistSqrdEnd-DistSqrdStart);
            printf("A maximum of %li hexagons found for a distance^2= %li - %.4f%% done\r", ctmax,  DstSqrdMax, 100*p);
            fflush(stdout);
        }
        if (!verboseDist & verboseEvery) 
            printf("A total of %li hexagons found for a distance^2= %li\n", ct,  DistanceSqrd);
        DistanceSqrd += (2 * (DistSqrd_n++) + 1) * DistSqrd_s;
    } while (DistanceSqrd < DistSqrdEnd);
    printf("Maximum number of hexagons found was %li for a distance^2=%li\n", ctmax, DstSqrdMax);
    return 0;
}
/* Fount 450 hexagons found for a distance^2=
   74266682763
  158640665547
  197701612563
  281637364827
  297066731052
  380385308667
  547148417907
  634562662188
  668400144867
  765502289643
  790806450252
  902092778643
  923498999787
 1096307901507
 1124208577947
 1126549459308
 1188266924208
 1283928994803
 1285083261147
 1427765989923
 1521541234668
 1735660299387
 1779314513067
 1856667069075
 1935665424147
 2182535283747
 2188593671628
 2281429304427
 2401415956443
 2444217334923
 2534736283443
 2538250648752
 2673600579468
 3062009158572
 3163225801008
 3318136637907
 3423467778003
 3492910748523
 3608371114572
 3693995999148
 3877372442307
 3966016638675
 3974810464443
 4161730388907
 4213834009707
 4385231606028
 4496834311788
 4506197837232
 4690733057283
 4753067696832
 4873348987563
 4924335761163
 4942540314075
 5002343826627
 5070912641067
 5135715979212
 5140333044588
 5465904416427
 5711063959692
 5858440199283
 6015601303803
 6086164938672
 6739752891963
 6889520606787
 6942641197548
 7040934120675
 7117258052268
 7426668276300
 7663046166867
 7742661696588
 7868603111187
 8118835007787
 8146911091683
 8311490998083
 8730141134988
 8754374686512
 8832248651667
 8889850120683
 8986268614323
 9106754693547
 9125717217708
 9159077516043
 9509632716675
 9605663825772 
 9776869339692 
 9866771113563 
 9958691247267 
10117877201523
10138945133772
10153002595008
10230492706707
10694402317872
10730808767523
10788418589403
11152720398603
11555360953227
11565749350323
11948706929523
12248036634288
12299773139787
12652903204032
12849893909307
12973097997363
13272546551628
13678710447675
13693871112012
13971642994092
14353723178067
14433484458288
14775983996592
15108641132403
15140327187027
15286656818667
15509489769228
15620942694483
15785064547707
15864066554700
15899241857772
16013830617603
16476300154587
16646921555628
16710003621675
16854639170187
16855336038828
17420988817323
17540926424112
17692064495427
17987337247152
18024791348928
18136664491323
18762932229132
19012270787328
19137557241075
19195520531187
19389364497867
19493395950252
19642817553723
19697343044652
19770161256300
20009375306508
20154661062627
20283650564268

gap here

12346266026754075

*/