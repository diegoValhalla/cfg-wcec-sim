/* stats.c */

/* 2012/09/28, Jan Gustafsson <jan.gustafsson@mdh.se>
 * Changes:
 *  - time is only enabled if the POUT flag is set
 *  - st.c:30:1:  main () warning: type specifier missing, defaults to 'int': fixed
 */

/* 2011/10/18, Benedikt Huber <benedikt@vmars.tuwien.ac.at>
 * Changes:
 *  - Measurement and Printing the Results is only enabled if the POUT flag is set
 *  - Added Prototypes for InitSeed and RandomInteger
 *  - Changed return type of InitSeed from 'missing (default int)' to 'void'
 */

#define MAX    10

/* Statistics Program:
 * This program computes for two arrays of numbers the sum, the
 * mean, the variance, and standard deviation.  It then determines the
 * correlation coefficient between the two arrays.
 */

int    Seed;
double ArrayA[MAX], ArrayB[MAX];
double SumA, SumB;
double Coef;

int main() {
    double MeanA, MeanB, VarA, VarB, StddevA, StddevB /*, Coef*/;

    Seed = 0;

    //Initialize(ArrayA);
    double *Array = ArrayA;
    int i2 = 0;
    while (i2 < MAX) { //@LOOP 10
        Seed = ((Seed * 133) + 81) % 8095;
        Array[i2] = i2 + Seed / 8095.0;
        i2++;
    }

    //Calc_Sum_Mean(ArrayA, &SumA, &MeanA);
    Array = ArrayA;
    double *Sum = &SumA;
    double *Mean = &MeanA;
    int i1;
    *Sum = 0;
    for (i1 = 0; i1 < MAX; i1++) {
        *Sum += Array[i1];
    }
    *Mean = *Sum / MAX;

    //Calc_Var_Stddev(ArrayA, MeanA, &VarA, &StddevA);
    Array = ArrayA;
    double mean = MeanA;
    double *Var = &VarA;
    double *Stddev = &StddevA;
    int    i8;
    double diffs;
    diffs = 0.0;
    i8     = 0;
    while (i8 < MAX) { //@LOOP 10
        double x = Array[i8] - mean;
        diffs += x * x;
        i8++;
    }
    *Var    = diffs / MAX;
    double val = *Var;
    float x2 = val / 10;
    float dx;
    double diff, tmp;
    double min_tol = 0.00001;
    int i5, flag;
    flag = 0;
    if (val == 0) {
        x2 = 0;
    }
    else {
        i5 = 1;
        while (i5 < 20) { //@LOOP 20
            if (!flag) {
                dx   = (val - (x2 * x2)) / (2.0 * x2);
                x2    = x2 + dx;
                diff = val - (x2 * x2);

                double n = diff;
                float f;
                if (n >= 0) {
                    f = n;
                }
                else{
                    f = -n;
                }
                tmp  = f;

                if (tmp <= min_tol) {
                    flag = 1;
                }
            }
            i5++;
        }
    }
    *Stddev = x2;

    //Initialize(ArrayB);
    Array = ArrayB;
    i2 = 0;
    while (i2 < MAX) { //@LOOP 10
        Seed = ((Seed * 133) + 81) % 8095;
        Array[i2] = i2 + Seed / 8095.0;
        i2++;
    }

    //Calc_Sum_Mean(ArrayB, &SumB, &MeanB);
    Array = ArrayB;
    Sum = &SumB;
    Mean = &MeanB;
    *Sum = 0;
    for (i1 = 0; i1 < MAX; i1++) {
        *Sum += Array[i1];
    }
    *Mean = *Sum / MAX;

    //Calc_Var_Stddev(ArrayB, MeanB, &VarB, &StddevB);
    Array = ArrayB;
    mean = MeanB;
    Var = &VarB;
    Stddev = &StddevB;
    diffs = 0.0;
    i8     = 0;
    while (i8 < MAX) { //@LOOP 10
        double x = Array[i8] - mean;
        diffs += x * x;
        i8++;
    }
    *Var    = diffs / MAX;
    val = *Var;
    x2 = val / 10;
    min_tol = 0.00001;
    flag = 0;
    if (val == 0) {
        x2 = 0;
    }
    else {
        i5 = 1;
        while (i5 < 20) { //@LOOP 20
            if (!flag) {
                dx   = (val - (x2 * x2)) / (2.0 * x2);
                x2    = x2 + dx;
                diff = val - (x2 * x2);

                double n = diff;
                float f;
                if (n >= 0) {
                    f = n;
                }
                else{
                    f = -n;
                }
                tmp  = f;

                if (tmp <= min_tol) {
                    flag = 1;
                }
            }
            i5++;
        }
    }
    *Stddev = x2;

    /* Coef will have to be used globally in Calc_LinCorrCoef since it would
     * be beyond the 6 registers used for passing parameters
     */
    //Calc_LinCorrCoef(ArrayA, ArrayB, MeanA, MeanB); {
    int    i;
    double numerator, Aterm, Bterm;

    numerator = 0.0;
    Aterm     = Bterm = 0.0;
    i         = 0;
    while (i < MAX) { //@LOOP 10
        numerator +=  (ArrayA[i] - MeanA) * (ArrayB[i] - MeanB);

        double x = ArrayA[i] - MeanA;
        Aterm     += x * x;

        x = ArrayB[i] - MeanB;
        Bterm     += x * x;

        i++;
    }
    // }

    /* Coef used globally */
    val = Aterm;
    x2 = val / 10;
    min_tol = 0.00001;
    flag = 0;
    if (val == 0) {
        x2 = 0;
    }
    else {
        i5 = 1;
        while (i5 < 20) { //@LOOP 20
            if (!flag) {
                dx   = (val - (x2 * x2)) / (2.0 * x2);
                x2    = x2 + dx;
                diff = val - (x2 * x2);

                double n = diff;
                float f;
                if (n >= 0) {
                    f = n;
                }
                else{
                    f = -n;
                }
                tmp  = f;

                if (tmp <= min_tol) {
                    flag = 1;
                }
            }
            i5++;
        }
    }
    float aterm_sqrt = x2;

    val = Bterm;
    x2 = val / 10;
    min_tol = 0.00001;
    flag = 0;
    if (val == 0) {
        x2 = 0;
    }
    else {
        i5 = 1;
        while (i5 < 20) { //@LOOP 20
            if (!flag) {
                dx   = (val - (x2 * x2)) / (2.0 * x2);
                x2    = x2 + dx;
                diff = val - (x2 * x2);

                double n = diff;
                float f;
                if (n >= 0) {
                    f = n;
                }
                else{
                    f = -n;
                }
                tmp  = f;

                if (tmp <= min_tol) {
                    flag = 1;
                }
            }
            i5++;
        }
    }
    float bterm_sqrt = x2;

    Coef = numerator / (aterm_sqrt * bterm_sqrt);

#ifdef POUT
    StopTime  = ttime();
    TotalTime = (StopTime - StartTime) / 1000.0;
    printf("     Sum A = %12.4f,      Sum B = %12.4f\n", SumA, SumB);
    printf("    Mean A = %12.4f,     Mean B = %12.4f\n", MeanA, MeanB);
    printf("Variance A = %12.4f, Variance B = %12.4f\n", VarA, VarB);
    printf(" Std Dev A = %12.4f, Variance B = %12.4f\n", StddevA, StddevB);
    printf("\nLinear Correlation Coefficient = %f\n", Coef);
#endif
}
