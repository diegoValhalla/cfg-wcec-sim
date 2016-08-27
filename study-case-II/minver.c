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
/*  FILE: minver.c                                                       */
/*  SOURCE : Turbo C Programming for Engineering by Hyun Soo Ahn         */
/*                                                                       */
/*  DESCRIPTION :                                                        */
/*                                                                       */
/*     Matrix inversion for 3x3 floating point matrix.                   */
/*                                                                       */
/*  REMARK :                                                             */
/*                                                                       */
/*  EXECUTION TIME :                                                     */
/*                                                                       */
/*                                                                       */
/*************************************************************************/


double a[3][3] =
{
	{ 3.0, -6.0,  7.0 },
	{ 9.0,	0.0, -5.0 },
	{ 5.0, -8.0,  6.0 },
};
double b[3][3], c[3][3], e[3][3], det;


int main() {
	int	   i2, j2;
	double eps;
	int	   seed = 0;

	eps = 1.0e-6;

	// get nondet matrices
	i2 = 0;
	while (i2 < 3) {     //@LOOP 3
		j2 = 0;
		while (j2 < 3) { //@LOOP 3
			seed	  = ((seed * 133) + 81) % 8095;
			a[i2][j2] = seed;

			seed	  = ((seed * 133) + 81) % 8095;
			b[i2][j2] = seed;
			j2++;
		}
		i2++;
	}

	// this inverts a
	int	   row = 3, col = 3;
	int	   work[500], i, j, k, r, iw, s, t, u, v;
	double w, wmax, pivot, api, w1;

	if ((row < 2) || (row > 500) || (eps <= 0.0)) {
		det = 999;
	}
	else {
		w1 = 1.0;
		i  = 0;
		while (i < row) { //@LOOP 3
			work[i] = i;
			i++;
		}

		k = 0;
		while (k < row) { //@LOOP 3
			wmax = 0.0;
			i	 = k;
			while (i < row) { //@LOOP 3
				double f, n = a[i][k];
				if (n >= 0) {
					f = n;
				}
				else {
					f = -n;
				}
				w = f;

				if (w > wmax) {
					wmax = w;
					r	 = i;
				}
				i++;
			}
			pivot = a[r][k];

			double f, n = a[i][k];
			if (n >= 0) {
				f = n;
			}
			else {
				f = -n;
			}
			api = f;

			if (api <= eps) {
				det = w1;
				k	= row + 2;
			}
			else {
				w1 *= pivot;
				u	= k * col;
				v	= r * col;
				if (r != k) {
					w1		= -w;
					iw		= work[k];
					work[k] = work[r];
					work[r] = iw;
					j		= 0;
					while (j < row) { //@LOOP 3
						s		= u + j;
						t		= v + j;
						w		= a[k][j];
						a[k][j] = a[r][j];
						a[r][j] = w;
						j++;
					}
				}

				i = 0;
				while (i < row) { //@LOOP 3
					a[k][i] /= pivot;
					i++;
				}

				i = 0;
				while (i < row) { //@LOOP 3
					if (i != k) {
						v = i * col;
						s = v + k;
						w = a[i][k];
						if (w != 0.0) {
							j = 0;
							while (j < row) { //@LOOP 3
								if (j != k) {
									a[i][j] -= w * a[k][j];
								}
								j++;
							}
							a[i][k] = -w / pivot;
						}
					}
					i++;
				}
				a[k][k] = 1.0 / pivot;
				k++;
			}
		}

		if (k != row + 2) {
			i = 0;
			while (i < row) { //@LOOP 3
				k = work[i];
				while (k != i) { //@LOOP 3
					iw		= work[k];
					work[k] = work[i];
					work[i] = iw;
					j		= 0;
					while (j < row) { //@LOOP 3
						u		= j * col;
						s		= u + i;
						t		= u + k;
						w		= a[k][i];
						a[k][i] = a[k][k];
						a[k][k] = w;
						j++;
					}
					k = work[i];
				}
				i++;
			}

			det = w1;

			int	   row_a = 3, row_b = 3;
			int	   col_a = 3, col_b = 3;
			int	   i3, j3, k3, row_c, col_c;
			double w3;

			row_c = row_a;
			col_c = col_b;

			if ((row_c < 1) || (row_b < 1) || (col_c < 1) || (col_a != row_b)) {
				det = 999;
			}
			else {
				i3 = 0;
				while (i3 < row_c) { //@LOOP 3
					j3 = 0;
					while (j3 < col_c) { //@LOOP 3
						w3 = 0.0;
						k3 = 0;
						while (k3 < row_b) { //@LOOP 3
							w3 += a[i3][k3] * b[k3][j3];
							k3++;
						}
						c[i3][j3] = w3;
						j3++;
					}
					i3++;
				}
			}
		}
	}
}
