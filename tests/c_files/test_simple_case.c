int main() {
    int a, b;

    a = 2;
    b = 3;
    if (a < b) {
        a += 2*b;
        a += 2*b;
        a *= 5;
    } else if (a > b) {
        a++;
        a *= 5;
    } else {
        a--;
    }

    while (a > b) { //@LOOP 5
        a--;
        if (a < b) {
            a += 2*b;
            a *= 5;
        } else {
            a += 2*b;
        }
    }

    while (a > b) { //@LOOP 6
        a--;
        if (a < b) {
            a += 2*b;
            a *= 5;
        } else {
            a += 2*b;
        }
    }

    if (a < b) {
        a += 2*b;
        a += 2*b;
        a *= 5;
    }

    return 0;
}
