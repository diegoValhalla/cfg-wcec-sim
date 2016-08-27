/*************************************************************************/
/*                                                                       */
/*   SNU-RT Benchmark Suite for Worst Case Timing Analysis               */
/*   =====================================================               */
/*                              Collected and Modified by S.-S. Lim      */
/*                                           sslim@archi.snu.ac.kr       */
/*                                         Real-Time Research Group      */
/*                                        Seoul National University      */
/*                                                                       */
/*                                                                       */
/*        < Features > - restrictions for our experimental environment   */
/*                                                                       */
/*          1. Completely structured.                                    */
/*               - There are no unconditional jumps.                     */
/*               - There are no exit from loop bodies.                   */
/*                 (There are no 'break' or 'return' in loop bodies)     */
/*          2. No 'switch' statements.                                   */
/*          3. No 'do..while' statements.                                */
/*          4. Expressions are restricted.                               */
/*               - There are no multiple expressions joined by 'or',     */
/*                'and' operations.                                      */
/*          5. No library calls.                                         */
/*               - All the functions needed are implemented in the       */
/*                 source file.                                          */
/*                                                                       */
/*                                                                       */
/*************************************************************************/
/*                                                                       */
/*  FILE: fir.c                                                          */
/*  SOURCE : C Algorithms for Real-Time DSP by P. M. Embree              */
/*                                                                       */
/*  DESCRIPTION :                                                        */
/*                                                                       */
/*     An example using FIR filter and Gaussian function.                */
/*     algorithm.                                                        */
/*     The function 'fir_filter' is for FIR filtering and the function   */
/*     'gaussian' is for Gaussian number generation.                     */
/*     The detailed description is above each function.                  */
/*                                                                       */
/*  REMARK :                                                             */
/*                                                                       */
/*  EXECUTION TIME :                                                     */
/*                                                                       */
/*                                                                       */
/*************************************************************************/

#define SAMPLE_RATE    11025
#define RAND_MAX       32768
#define PI             3.14159265358979323846

float fir_lpf35[35] =
{
    -6.3600959e-03, -7.6626200e-05, 7.6912856e-03,  5.0564148e-03, -8.3598122e-03,
    -1.0400905e-02,  8.6960020e-03, 2.0170502e-02, -2.7560785e-03, -3.0034777e-02,
    -8.9075034e-03,  4.1715767e-02, 3.4108155e-02, -5.0732918e-02, -8.6097546e-02,
    5.7914939e-02,   3.1170085e-01, 4.4029310e-01,  3.1170085e-01,  5.7914939e-02,
    -8.6097546e-02, -5.0732918e-02, 3.4108155e-02,  4.1715767e-02, -8.9075034e-03,
    -3.0034777e-02, -2.7560785e-03, 2.0170502e-02,  8.6960020e-03, -1.0400905e-02,
    -8.3598122e-03,  5.0564148e-03, 7.6912856e-03, -7.6626200e-05, -6.3600959e-03
};

float fir_lpf37[37] =
{
    -6.51000e-04, -3.69500e-03, -6.28000e-04, 6.25500e-03,  4.06300e-03,
    -8.18900e-03, -1.01860e-02,  7.84700e-03, 1.89680e-02, -3.05100e-03,
    -2.96620e-02, -9.06500e-03,  4.08590e-02, 3.34840e-02, -5.07550e-02,
    -8.61070e-02,  5.75690e-02,  3.11305e-01, 4.40000e-01,  3.11305e-01,
    5.75690e-02,  -8.61070e-02, -5.07550e-02, 3.34840e-02,  4.08590e-02,
    -9.06500e-03, -2.96620e-02, -3.05100e-03, 1.89680e-02,  7.84700e-03,
    -1.01860e-02, -8.18900e-03,  4.06300e-03, 6.25500e-03, -6.28000e-04,
    -3.69500e-03, -6.51000e-04
};

int main() {
    unsigned long next;
    float sigma = 0.2;
    int          i;
    float        x, var_sin, var_gaussian;
    static float hist[34];

    next = 1;
    /* first with filter */
    i = 0;
    while (i < 10) { //@LOOP 10
        //var_sin = sin(0.05 * 2 * PI * i);
        double rad = 0.05 * 2 * PI * i;
        float app;

        float diff;
        float tmp;
        int   inc = 1;

        while (rad > 2 * PI) { //@LOOP 5
            rad -= 2 * PI;
        }

        while (rad < -2 * PI) { //@LOOP 2
            rad += 2 * PI;
        }

        app  = diff = rad;
        diff = (diff * (-(rad * rad))) /
               ((2.0 * inc) * (2.0 * inc + 1.0));
        app = app + diff;
        inc++;

        //tmp = fabs(diff);
        double n = diff;
        float f;
        if (n >= 0) {
            f = n;
        }
        else {
            f = -n;
        }
        tmp = f;

        while (tmp >= 0.00001) { //@LOOP 5
            diff = (diff * (-(rad * rad))) /
                   ((2.0 * inc) * (2.0 * inc + 1.0));
            app = app + diff;
            inc++;
            //tmp = fabs(diff);
            n = diff;
            if (n >= 0) {
                f = n;
            }
            else {
                f = -n;
            }
            tmp = f;
        }
        var_sin = app;

        //var_gaussian = gaussian();
        static int   ready = 0;     /* flag to indicated stored value */
        static float gstore;        /* place to store other value */
        static float rconst1 = (float)(2.0 / RAND_MAX);
        static float rconst2 = (float)(RAND_MAX / 2.0);
        float        v1, v2, r, fac;
        float        gaus;

    /* make two numbers if none stored */
        if (ready == 0) {
            next = next * 1103515245 + 12345;
            v1  = (float)((unsigned int)(next / 65536) % 32768) - rconst2;

            next = next * 1103515245 + 12345;
            v2  = (float)((unsigned int)(next / 65536) % 32768) - rconst2;

            v1 *= rconst1;
            v2 *= rconst1;
            r   = v1 * v1 + v2 * v2;
            while (r > 1.0f) { //@LOOP 10
                next = next * 1103515245 + 12345;
                v1  = (float)((unsigned int)(next / 65536) % 32768) - rconst2;

                next = next * 1103515245 + 12345;
                v2  = (float)((unsigned int)(next / 65536) % 32768) - rconst2;

                v1 *= rconst1;
                v2 *= rconst1;
                r   = v1 * v1 + v2 * v2;
            }      /* make radius less than 1 */

    /* remap v1 and v2 to two Gaussian numbers */
            /*        fac = sqrt(-2.0f*log(r)/r);  */

            //fac    = sqrt(-2.0f * 0.1);
            double val = -2.0f * 0.1;
            float x = val / 10;

            float dx;

            double diff, tmp;
            double min_tol = 0.00001;

            int j, flag;

            flag = 0;
            if (val == 0) {
                x = 0;
            }
            else {
                j = 1;
                while (j < 20) { //@LOOP 20
                    if (!flag) {
                        dx   = (val - (x * x)) / (2.0 * x);
                        x    = x + dx;
                        diff = val - (x * x);

                        //tmp = fabs(diff);
                        double n = diff;
                        float f;
                        if (n >= 0) {
                            f = n;
                        }
                        else {
                            f = -n;
                        }
                        tmp = f;

                        if (tmp <= min_tol) {
                            flag = 1;
                        }
                    }
                    j++;
                }
            }
            fac = x;

            gstore = v1 * fac;      /* store one */
            gaus   = v2 * fac;      /* return one */
            ready  = 1;             /* set ready flag */
        }

        else {
            ready = 0;      /* reset ready flag for next pair */
            gaus  = gstore; /* return the stored one */
        }
        var_gaussian = gaus;

        x = var_sin + sigma * var_gaussian;

        x *= 25000.0;       /* scale for D/A converter */

        //fir_filter(x, fir_lpf35, 35, hist);
        float input = x;
        float *coef = fir_lpf35;
        int n2 = 35;
        float *history = hist;
        float *hist_ptr, *hist1_ptr, *coef_ptr;
        float output;

        hist_ptr  = history;
        hist1_ptr = hist_ptr;             /* use for history update */
        coef_ptr  = coef + n2 - 1;         /* point to last coef */

        /* form output accumulation */
        output = *hist_ptr++ *(*coef_ptr--);
        int j = 2;
        while (j < n2) { //@LOOP 35
            *hist1_ptr++ = *hist_ptr;            /* update history array */
            output      += (*hist_ptr++) * (*coef_ptr--);
            j++;
        }
        output    += input * (*coef_ptr);        /* input tap */
        *hist1_ptr = input;                      /* last history */

        i++;
    }

    /* now without filter */
    i = 0;
    while (i < 10) { //@LOOP 10
        //var_sin = sin(0.05 * 2 * PI * i);
        double rad = 0.05 * 2 * PI * i;
        float app;

        float diff;
        float tmp;
        int   inc = 1;

        while (rad > 2 * PI) { //@LOOP 5
            rad -= 2 * PI;
        }

        while (rad < -2 * PI) { //@LOOP 2
            rad += 2 * PI;
        }

        app  = diff = rad;
        diff = (diff * (-(rad * rad))) /
               ((2.0 * inc) * (2.0 * inc + 1.0));
        app = app + diff;
        inc++;

        //tmp = fabs(diff);
        double n = diff;
        float f;
        if (n >= 0) {
            f = n;
        }
        else {
            f = -n;
        }
        tmp = f;

        while (tmp >= 0.00001) { //@LOOP 5
            diff = (diff * (-(rad * rad))) /
                   ((2.0 * inc) * (2.0 * inc + 1.0));
            app = app + diff;
            inc++;
            //tmp = fabs(diff);
            n = diff;
            if (n >= 0) {
                f = n;
            }
            else {
                f = -n;
            }
            tmp = f;
        }
        var_sin = app;

        //var_gaussian = gaussian();
        static int   ready = 0;     /* flag to indicated stored value */
        static float gstore;        /* place to store other value */
        static float rconst1 = (float)(2.0 / RAND_MAX);
        static float rconst2 = (float)(RAND_MAX / 2.0);
        float        v1, v2, r, fac;
        float        gaus;

    /* make two numbers if none stored */
        if (ready == 0) {
            next = next * 1103515245 + 12345;
            v1  = (float)((unsigned int)(next / 65536) % 32768) - rconst2;

            next = next * 1103515245 + 12345;
            v2  = (float)((unsigned int)(next / 65536) % 32768) - rconst2;

            v1 *= rconst1;
            v2 *= rconst1;
            r   = v1 * v1 + v2 * v2;
            while (r > 1.0f) { //@LOOP 10
                next = next * 1103515245 + 12345;
                v1  = (float)((unsigned int)(next / 65536) % 32768) - rconst2;

                next = next * 1103515245 + 12345;
                v2  = (float)((unsigned int)(next / 65536) % 32768) - rconst2;

                v1 *= rconst1;
                v2 *= rconst1;
                r   = v1 * v1 + v2 * v2;
            }      /* make radius less than 1 */

    /* remap v1 and v2 to two Gaussian numbers */
            /*        fac = sqrt(-2.0f*log(r)/r);  */

            //fac    = sqrt(-2.0f * 0.1);
            double val = -2.0f * 0.1;
            float x = val / 10;

            float dx;

            double diff, tmp;
            double min_tol = 0.00001;

            int j, flag;

            flag = 0;
            if (val == 0) {
                x = 0;
            }
            else {
                j = 1;
                while (j < 20) { //@LOOP 20
                    if (!flag) {
                        dx   = (val - (x * x)) / (2.0 * x);
                        x    = x + dx;
                        diff = val - (x * x);

                        //tmp = fabs(diff);
                        double n = diff;
                        float f;
                        if (n >= 0) {
                            f = n;
                        }
                        else {
                            f = -n;
                        }
                        tmp = f;

                        if (tmp <= min_tol) {
                            flag = 1;
                        }
                    }
                    j++;
                }
            }
            fac = x;

            gstore = v1 * fac;      /* store one */
            gaus   = v2 * fac;      /* return one */
            ready  = 1;             /* set ready flag */
        }

        else {
            ready = 0;      /* reset ready flag for next pair */
            gaus  = gstore; /* return the stored one */
        }
        var_gaussian = gaus;

        x = var_sin + sigma * var_gaussian;

        x *= 25000.0;       /* scale for D/A converter */
        i++;
    }

    return 0;
}
