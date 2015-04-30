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
/*  FILE: fft1.c                                                         */
/*  SOURCE : Turbo C Programming for Engineering by Hyun Soon Ahn        */
/*                                                                       */
/*  DESCRIPTION :                                                        */
/*                                                                       */
/*     FFT using Cooly-Turkey algorithm.                                 */
/*     There are two inputs, ar[] and ai[]. ar[] is real number parts    */
/*     of input array and the ai[] is imaginary number parts of input.   */
/*     The function fft1 process FFT or inverse FFT according to the    .*/
/*     parameter flag. (FFT with flag=0, inverse FFT with flag=1).       */
/*                                                                       */
/*                                                                       */
/*  REMARK :                                                             */
/*                                                                       */
/*  EXECUTION TIME :                                                     */
/*                                                                       */
/*                                                                       */
/*************************************************************************/


#define DEBUG
#define PI      3.14159
#define M_PI    3.14159
#define N 8

double ar[N];
double ai[N] = { 0., };

int main() {
    int i, n = N, flag, chkerr;

    /* ar  */
    i = 0;
    while (i < n) { //@LOOP 8
        // ------------------------------------
        //ar[i] = cos(2 * M_PI * i / n);
        double rad = 2 * M_PI * i / n;

        // ------------------------------------
        //ar[i] = sin(PI / 2.0 - rad);
        rad = PI / 2.0 - rad;
        double app;
        double tmp;

        double diff;
        int    inc = 1;

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
        double n = diff, f;
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

        ar[i] = app;
        // ------------------------------------
        // ------------------------------------

        i++;
    }

    /* forward fft */
    flag   = 0;
    //chkerr = fft1(n, flag);
    int    j, k, it, xp, xp2, j1, j2, iter;
    double sign, w, wr, wi, dr1, dr2, di1, di2, tr, ti, arg;
    int result = 0;

    if (n < 2) {
        result = 999;
    } else {

        iter = 10;
        j    = 1;

        i = 0;
        while (i < iter) { //@LOOP 10
            j *= 2;
            i++;
        }

            /*  Main FFT Loops  */
            if (flag) {
                sign = 1.0;
            } else {
                sign = -1.0;
            }

            xp2  = n;
            it = 0;
            while (it < iter) { //@LOOP 10
                xp   = xp2;
                xp2 /= 2;
                w    = PI / xp2;

                k = 0;
                while (k < xp2) { //@LOOP 10
                    arg = k * w;
                    //wr  = cos(arg);
                    // ------------------------------------
                    double rad = arg;
                    //wr = sin(PI / 2.0 - rad);
                    rad = PI / 2.0 - rad;
                    double app;
                    double tmp;

                    double diff;
                    int    inc = 1;

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
                    double n = diff, f;
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

                    wr = app;
                    // ------------------------------------


                    //wi  = sign * sin(arg);
                    // ------------------------------------
                    rad = arg;
                    inc = 1;

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
                    n = diff;
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
                    wi = sign * app;
                    // ------------------------------------

                    i   = k - xp;
                    j = xp;
                    while (j <= n) { //@LOOP 10
                        j1     = j + i;
                        j2     = j1 + xp2;
                        dr1    = ar[j1];
                        dr2    = ar[j2];
                        di1    = ai[j1];
                        di2    = ai[j2];
                        tr     = dr1 - dr2;
                        ti     = di1 - di2;
                        ar[j1] = dr1 + dr2;
                        ai[j1] = di1 + di2;
                        ar[j2] = tr * wr - ti * wi;
                        ai[j2] = ti * wr + tr * wi;
                        j += xp;
                    }
                    k++;
                }
                it++;
            }

            /*  Digit Reverse Counter  */
            j1 = n / 2;
            j2 = n - 1;
            j  = 1;

            i = 1;
            while (i <= j2) { //@LOOP 7
                if (i < j) {
                    tr        = ar[j - 1];
                    ti        = ai[j - 1];
                    ar[j - 1] = ar[i - 1];
                    ai[j - 1] = ai[i - 1];
                    ar[i - 1] = tr;
                    ai[i - 1] = ti;
                }
                k = j1;
                while (k < j) { //@LOOP 4
                    j -= k;
                    k /= 2;
                }
                j += k;
                i++;
            }

            if (flag != 0) {
                w = n;
                i = 0;
                while (i < n) { //@LOOP 8
                    ar[i] /= w;
                    ai[i] /= w;
                    i++;
                }
            }
    }

    chkerr = result;

    /* inverse fft */
    flag   = 1;
    //chkerr = fft1(n, flag);
    result = 0;

    if (n < 2) {
        result = 999;
    } else {

        iter = 10;
        j    = 1;

        i = 0;
        while (i < iter) { //@LOOP 10
            j *= 2;
            i++;
        }

            /*  Main FFT Loops  */
            if (flag) {
                sign = 1.0;
            } else {
                sign = -1.0;
            }

            xp2  = n;
            it = 0;
            while (it < iter) { //@LOOP 10
                xp   = xp2;
                xp2 /= 2;
                w    = PI / xp2;

                k = 0;
                while (k < xp2) { //@LOOP 10
                    arg = k * w;
                    //wr  = cos(arg);
                    // ------------------------------------
                    double rad = arg;
                    //wr = sin(PI / 2.0 - rad);
                    rad = PI / 2.0 - rad;
                    double app;
                    double tmp;

                    double diff;
                    int    inc = 1;

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
                    double n = diff, f;
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

                    wr = app;
                    // ------------------------------------


                    //wi  = sign * sin(arg);
                    // ------------------------------------
                    rad = arg;
                    inc = 1;

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
                    n = diff;
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
                    wi = sign * app;
                    // ------------------------------------

                    i   = k - xp;
                    j = xp;
                    while (j <= n) { //@LOOP 10
                        j1     = j + i;
                        j2     = j1 + xp2;
                        dr1    = ar[j1];
                        dr2    = ar[j2];
                        di1    = ai[j1];
                        di2    = ai[j2];
                        tr     = dr1 - dr2;
                        ti     = di1 - di2;
                        ar[j1] = dr1 + dr2;
                        ai[j1] = di1 + di2;
                        ar[j2] = tr * wr - ti * wi;
                        ai[j2] = ti * wr + tr * wi;
                        j += xp;
                    }
                    k++;
                }
                it++;
            }

            /*  Digit Reverse Counter  */
            j1 = n / 2;
            j2 = n - 1;
            j  = 1;

            i = 1;
            while (i <= j2) { //@LOOP 7
                if (i < j) {
                    tr        = ar[j - 1];
                    ti        = ai[j - 1];
                    ar[j - 1] = ar[i - 1];
                    ai[j - 1] = ai[i - 1];
                    ar[i - 1] = tr;
                    ai[i - 1] = ti;
                }
                k = j1;
                while (k < j) { //@LOOP 4
                    j -= k;
                    k /= 2;
                }
                j += k;
                i++;
            }

            if (flag != 0) {
                w = n;
                i = 0;
                while (i < n) { //@LOOP 8
                    ar[i] /= w;
                    ai[i] /= w;
                    i++;
                }
            }
    }
    chkerr = result;

    return 0;
}
