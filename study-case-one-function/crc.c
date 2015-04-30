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
/*  FILE: crc.c                                                          */
/*  SOURCE : Numerical Recipes in C - The Second Edition                 */
/*                                                                       */
/*  DESCRIPTION :                                                        */
/*                                                                       */
/*     A demonstration for CRC (Cyclic Redundancy Check) operation.      */
/*     The CRC is manipulated as two functions, icrc1 and icrc.          */
/*     icrc1 is for one character and icrc uses icrc1 for a string.      */
/*     The input string is stored in array lin[].                        */
/*     icrc is called two times, one for X-Modem string CRC and the      */
/*     other for X-Modem packet CRC.                                     */
/*                                                                       */
/*  REMARK :                                                             */
/*                                                                       */
/*  EXECUTION TIME :                                                     */
/*                                                                       */
/*                                                                       */
/*************************************************************************/

typedef unsigned char uchar;

int main(void) {
    unsigned char lin[256] = "asdffeagewaHAFEFaeDsFEawFdsFaefaeerdjgp";
    unsigned short i1, i2;
    unsigned long  n;

    // >>>>>>>> for i1
    n          = 40;
    lin[n + 1] = 0;
    //i1         = icrc(0, n, (short)0, 1);
    unsigned short crc = 0;
    unsigned long len = n;
    short jinit = 0;
    int jrev = 1;

    static unsigned short icrctb[256], init = 0;
    static uchar rchr[256];
    unsigned short tmp1, tmp2, j, cword = crc;
    static uchar it[16] = { 0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15 };

    if (!init) {
        init = 1;
        j = 0;
        while (j <= 255) { //@LOOP 255

            //icrctb[j] = icrc1(j << 8, (uchar)0);
            unsigned short crc1 = j << 8;
            unsigned char onech = 0;
            int idx1 = 0;
            unsigned short ans = (crc1 ^ onech << 8);

            while (idx1 < 8) { //@LOOP 8
                if (ans & 0x8000) {
                    ans = (ans <<= 1) ^ 4129;
                }
                else {
                    ans <<= 1;
                }

                idx1++;
            }
            icrctb[j] = ans;

            rchr[j]   = (uchar)(it[j & 0xF] << 4 | it[j >> 4]);
            j++;
        }
    }

    if (jinit >= 0) {
        cword = ((uchar)jinit) | (((uchar)jinit) << 8);
    }
    else if (jrev < 0) {
        cword = rchr[(uchar)(cword >> 8)] | rchr[(uchar)(cword & 0xFF)] << 8;
    }

    j = 1;
    while (j <= len) { //@LOOP 42
        if (jrev < 0) {
            tmp1 = rchr[lin[j]] ^ ((uchar)(cword >> 8));
        }
        else {
            tmp1 = lin[j] ^ ((uchar)(cword >> 8));
        }
        cword = icrctb[tmp1] ^ ((uchar)(cword & 0xFF)) << 8;

        j++;
    }

    if (jrev >= 0) {
        tmp2 = cword;
    }
    else {
        tmp2 = rchr[(uchar)(cword >> 8)] | rchr[(uchar)(cword & 0xFF)] << 8;
    }
    i1 = tmp2;


    // >>>>>>>> for i2
    lin[n + 1] = (uchar)(i1 >> 8);
    lin[n + 2] = (uchar)(i1 & 0xFF);
    //i2         = icrc(i1, n + 2, (short)0, 1);
    crc = i1;
    len = n + 2;
    jinit = 0;
    jrev = 1;

    init = 0;
    cword = crc;

    if (!init) {
        init = 1;
        j = 0;
        while (j <= 255) { //@LOOP 255

            //icrctb[j] = icrc1(j << 8, (uchar)0);
            unsigned short crc1 = j << 8;
            unsigned char onech = 0;
            int idx1 = 0;
            unsigned short ans = (crc1 ^ onech << 8);

            while (idx1 < 8) { //@LOOP 8
                if (ans & 0x8000) {
                    ans = (ans <<= 1) ^ 4129;
                }
                else {
                    ans <<= 1;
                }

                idx1++;
            }
            icrctb[j] = ans;

            rchr[j]   = (uchar)(it[j & 0xF] << 4 | it[j >> 4]);
            j++;
        }
    }

    if (jinit >= 0) {
        cword = ((uchar)jinit) | (((uchar)jinit) << 8);
    }
    else if (jrev < 0) {
        cword = rchr[(uchar)(cword >> 8)] | rchr[(uchar)(cword & 0xFF)] << 8;
    }

    j = 1;
    while (j <= len) { //@LOOP 42
        if (jrev < 0) {
            tmp1 = rchr[lin[j]] ^ ((uchar)(cword >> 8));
        }
        else {
            tmp1 = lin[j] ^ ((uchar)(cword >> 8));
        }
        cword = icrctb[tmp1] ^ ((uchar)(cword & 0xFF)) << 8;

        j++;
    }

    if (jrev >= 0) {
        tmp2 = cword;
    }
    else {
        tmp2 = rchr[(uchar)(cword >> 8)] | rchr[(uchar)(cword & 0xFF)] << 8;
    }
    i2 = tmp2;

    return(0);
}
