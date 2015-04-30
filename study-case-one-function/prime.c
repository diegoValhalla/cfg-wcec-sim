/* MDH WCET BENCHMARK SUITE. */

/* Changes:
 * JG 2005/12/08: Prototypes added, and changed exit to return in main.
 */

int main() {
    unsigned int x = 21649;
    unsigned int y = 513239;
    unsigned int tmp, i;
    unsigned char result_x, result_y, result;

    // swap
    tmp = x;
    x = y;
    y = tmp;

    // check if x is prime
    if (x == 2) {
        result_x = 1;
    } else if (x % 2 == 0) {
        result_x = 0;
    } else {
        i = 3;
        while (i * i <= x) { //@LOOP 65535
            if (x % i == 0) {
                result_x = 0;
                x = 0;
            } else {
                i += 2;
            }
        }

        if (x % i != 0) {
            result_x = 1;
        }
    }

    // check if y is prime
    // y number was removed, because it was taking too long
    // to compute all possible paths of this CFG
    /*
    if (y == 2) {
        result_y = 1;
    } else if (y % 2 == 0) {
        result_y = 0;
    } else {
        i = 3;
        while (i * i <= y) { //@LOOP 65535
            if (y % i == 0) {
                result_y = 0;
                y = 0;
            } else {
                i += 2;
            }
        }

        if (y % i != 0) {
            result_y = 1;
        }
    }

    result = result_x & result_y;
    */

    result = result_x;

    if (result) {
        result = 0;
    } else {
        result = 1;
    }

    return result;
}
