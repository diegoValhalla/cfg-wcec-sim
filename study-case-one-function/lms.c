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
/*  FILE: lms.c                                                          */
/*  SOURCE : C Algorithms for Real-Time DSP by P. M. Embree              */
/*                                                                       */
/*  DESCRIPTION :                                                        */
/*                                                                       */
/*     An LMS adaptive signal enhancement. The input signal is a sine    */
/*     wave with added white noise.                                      */
/*     The detailed description is in the program source code.           */
/*                                                                       */
/*  REMARK :                                                             */
/*                                                                       */
/*  EXECUTION TIME :                                                     */
/*                                                                       */
/*                                                                       */
/*************************************************************************/

#define RAND_MAX    32768
#define PI          3.14159265358979323846

/* function prototypes for fft and filter functions */

#define N    201
#define L    20         /* filter order, (length L+1) */

/* set convergence parameter */
float mu = 0.01;
unsigned long next;

int main() {
    static float d[N], b[21];
    float        signal_amp, noise_amp, arg, x;
    int          k;
    next = 1;

/* create signal plus noise */
    //signal_amp = sqrt(2.0);
    double val = 2.0f;
    x = val / 10;
    float dx;
    double diff;
    double min_tol = 0.00001;
    int i, flag;

    flag = 0;
    if (val == 0) {
        x = 0;
    }
    else {
        i = 1;
        while (i < 20) { //@LOOP 20
            if (!flag) {
                dx   = (val - (x * x)) / (2.0 * x);
                x    = x + dx;
                diff = val - (x * x);

                double n = diff;
                float f;
                if (n >= 0) {
                    f = n;
                }
                else{
                    f = -n;
                }
                n = f;

                if (n <= min_tol) {
                    flag = 1;
                }
            }
            i++;
        }
    }
    signal_amp = x;

    //noise_amp  = 0.2 * sqrt(12.0);
    val = 12.0f;
    x = val / 10;
    min_tol = 0.00001;
    flag = 0;

    if (val == 0) {
        x = 0;
    }
    else {
        i = 1;
        while (i < 20) { //@LOOP 20
            if (!flag) {
                dx   = (val - (x * x)) / (2.0 * x);
                x    = x + dx;
                diff = val - (x * x);

                double n = diff;
                float f;
                if (n >= 0) {
                    f = n;
                }
                else{
                    f = -n;
                }
                n = f;

                if (n <= min_tol) {
                    flag = 1;
                }
            }
            i++;
        }
    }
    noise_amp = 0.2 * x;

    arg        = 2.0 * PI / 20.0;
    k          = 0;
    while (k < N) { //@LOOP 201

        double rad = arg * k;
        float app;
        float diff;
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

        double n = diff;
        float f;
        if (n >= 0) {
            f = n;
        }
        else {
            f = -n;
        }
        n = f;

        while (n >= 0.00001) { //@LOOP 5
            diff = (diff * (-(rad * rad))) /
                   ((2.0 * inc) * (2.0 * inc + 1.0));
            app = app + diff;
            inc++;

            n = diff;
            if (n >= 0) {
                f = n;
            }
            else {
                f = -n;
            }
            n = f;
        }
        n = app;

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
            while (r > 1.0f) { //@LOOP 5
                next = next * 1103515245 + 12345;
                v1  = (float)((unsigned int)(next / 65536) % 32768) - rconst2;

                next = next * 1103515245 + 12345;
                v2  = (float)((unsigned int)(next / 65536) % 32768) - rconst2;

                v1 *= rconst1;
                v2 *= rconst1;
                r   = v1 * v1 + v2 * v2;
            }       /* make radius less than 1 */

    /* remap v1 and v2 to two Gaussian numbers */
            //fac    = sqrt(-2.0f * 4.5 / r);
            double val = -2.0f * 4.5 / r;
            float x = val / 10;
            float dx;
            double diff;
            double min_tol = 0.00001;
            int i, flag;

            flag = 0;
            if (val == 0) {
                x = 0;
            }
            else {
                i = 1;
                while (i < 20) { //@LOOP 20
                    if (!flag) {
                        dx   = (val - (x * x)) / (2.0 * x);
                        x    = x + dx;
                        diff = val - (x * x);

                        double n = diff;
                        float f;
                        if (n >= 0) {
                            f = n;
                        }
                        else{
                            f = -n;
                        }
                        n = f;

                        if (n <= min_tol) {
                            flag = 1;
                        }
                    }
                    i++;
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

        d[k] = signal_amp * n + noise_amp * gaus;

        k++;
    }

/* scale based on L */
    mu = 2.0 * mu / (L + 1);

    x = 0.0;
    k = 0;
    while (k < N) { //@LOOP 201
        //for(k = 0 ; k < N ; k++) {
        //lms(x, d[k], b, L, mu, 0.01);
        float d1 = d[k];
        int l = L;
        float alpha = 0.01;

        int          ll;
        float        e, mu_e, y;
        static float px[51];      /* max L = 50 */
        static float sigma = 2.0; /* start at 2 and update internally */

        px[0] = x;

    /* calculate filter output */
        y  = b[0] * px[0];
        ll = 1;
        while (ll <= l) { //@LOOP 20
            //for(ll = 1 ; ll <= l ; ll++)
            y = y + b[ll] * px[ll];
            ll++;
        }

    /* error signal */
        e = d1 - y;

    /* update sigma */
        sigma = alpha * (px[0] * px[0]) + (1 - alpha) * sigma;
        mu_e  = mu * e / sigma;

    /* update coefficients */
        ll = 0;
        while (ll <= l) { //@LOOP 20
            //for(ll = 0 ; ll <= l ; ll++)
            b[ll] = b[ll] + mu_e * px[ll];
            ll++;
        }

    /* update history */
        ll = l;
        while (ll >= 1) { //@LOOP 20
            //for(ll = l ; ll >= 1 ; ll--)
            px[ll] = px[ll - 1];
            ll--;
        }

/* delay x one sample */
        x = d[k];
        k++;
    }

    return(0);
}
