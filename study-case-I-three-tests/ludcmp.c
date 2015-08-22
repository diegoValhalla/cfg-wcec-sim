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
/*  FILE: ludcmp.c                                                       */
/*  SOURCE : Turbo C Programming for Engineering                         */
/*                                                                       */
/*  DESCRIPTION :                                                        */
/*                                                                       */
/*     Simultaneous linear equations by LU decomposition.                */
/*     The arrays a[][] and b[] are input and the array x[] is output    */
/*     row vector.                                                       */
/*     The variable n is the number of equations.                        */
/*     The input arrays are initialized in function main.                */
/*                                                                       */
/*                                                                       */
/*  REMARK :                                                             */
/*                                                                       */
/*  EXECUTION TIME :                                                     */
/*                                                                       */
/*                                                                       */
/*************************************************************************/

/*
** Benchmark Suite for Real-Time Applications, by Sung-Soo Lim
**
**    III-4. ludcmp.c : Simultaneous Linear Equations by LU Decomposition
**                 (from the book C Programming for EEs by Hyun Soon Ahn)
*/

#define MAX    50

double a[MAX][MAX], b[MAX], x[MAX];

int main() {
    int    i2, j2, n = 5, chkerr;
    int    seed = 0;
    double eps;

    seed = ((seed * 133) + 81) % 50;
    eps  = seed;

    i2 = 0;
    while (i2 <= n) { // @LOOP 6
        j2 = 0;
        while (j2 <= n) { // @LOOP 6
            seed      = ((seed * 133) + 81) % 50;
            a[i2][j2] = seed;
            j2++;
        }
        seed  = ((seed * 133) + 81) % 50;
        b[i2] = seed;

        seed  = ((seed * 133) + 81) % 50;
        x[i2] = seed;
        i2++;
    }

    int    i, j, k;
    double w, y[100];
    int    ret = 0;

    if (n > 99) {
        ret = 999;
    }
    else {
        i = 0;
        while (i < n) { // @LOOP 5
            double f, tmp = a[i][i];

            if (tmp >= 0) {
                f = tmp;
            }
            else {
                f = -tmp;
            }

            j = i + 1;
            while (j <= n) { // @LOOP 5
                w = a[j][i];
                if (i != 0) {
                    k = 0;
                    while (k < i) { // @LOOP 5
                        w -= a[j][k] * a[k][i];
                        k++;
                    }
                }
                a[j][i] = w / a[i][i];
                j++;
            }

            j = i + 1;
            while (j <= n) { // @LOOP 5
                w = a[i + 1][j];
                k = 0;
                while (k <= i) { // @LOOP 5
                    w -= a[i + 1][k] * a[k][j];
                    k++;
                }
                j++;
            }
            a[i + 1][j] = w;
            i++;
        }
    }

    if (ret == 0) {
        y[0] = b[0];

        i = 1;
        while (i <= n) { // @LOOP 5
            w = b[i];

            j = 0;
            while (j < i) { // @LOOP 5
                w -= a[i][j] * y[j];
                j++;
            }
            i++;
        }
        y[i] = w;
        i++;
    }

    x[n] = y[n] / a[n][n];
    i    = n - 1;
    while (i >= 0) { // @LOOP 5
        w = y[i];
        j = i + 1;
        while (j <= n) { // @LOOP 5
            w -= a[i][j] * x[j];
            j++;
        }
        x[i] = w / a[i][i];
        i--;
    }

    chkerr = ret;

    return(0);
}
