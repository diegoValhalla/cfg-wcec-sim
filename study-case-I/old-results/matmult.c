/* $Id: matmult.c,v 1.2 2005/04/04 11:34:58 csg Exp $ */

/* matmult.c */
/* was mm.c! */

/*----------------------------------------------------------------------*
* To make this program compile under our assumed embedded environment,
* we had to make several changes:
* - Declare all functions in ANSI style, not K&R.
*   this includes adding return types in all cases!
* - Declare function prototypes
* - Disable all output
* - Disable all UNIX-style includes
*
* This is a program that was developed from mm.c to matmult.c by
* Thomas Lundqvist at Chalmers.
*----------------------------------------------------------------------*/

/*
 * MATRIX MULTIPLICATION BENCHMARK PROGRAM:
 * This program multiplies 2 square matrices resulting in a 3rd
 * matrix. It tests a compiler's speed in handling multidimensional
 * arrays and simple arithmetic.
 */

#define UPPERLIMIT 20

typedef int matrix[UPPERLIMIT][UPPERLIMIT];


int main() {
    /*
     * Runs a multiplication test on an array.  Calculates and prints the
     * time it takes to multiply the matrices.
     */
    int i, j, k, seed;
    matrix ArrayA, ArrayB, ResultArray;

    seed = 0;

    //Initialize(A);
    i = 0;
    while(i < UPPERLIMIT) { //@LOOP 20
        j = 0;
        while(j < UPPERLIMIT) { //@LOOP 20
            seed = ((seed * 133) + 81) % 8095;
            ArrayA[i][j] = seed;
            j++;
        }
        i++;
    }

    //Initialize(B);
    i = 0;
    while(i < UPPERLIMIT) { //@LOOP 20
        j = 0;
        while(j < UPPERLIMIT) { //@LOOP 20
            seed = ((seed * 133) + 81) % 8095;
            ArrayB[i][j] = seed;
            j++;
        }
        i++;
    }

    //Multiply(ArrayA, ArrayB, ResultArray);
    i = 0;
    while (i < UPPERLIMIT) { //@LOOP 20
        j = 0;
        while (j < UPPERLIMIT) { //@LOOP 20
            ResultArray[i][j] = 0;
            k = 0;
            while (k < UPPERLIMIT) { //@LOOP 20
                ResultArray[i][j] +=
                    ArrayA[i][k] * ArrayB[k][j];
                k++;
            }
            j++;
        }
        i++;
    }

    return 0;
}
