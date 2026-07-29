typedef struct {
    char pad[52];
    unsigned char p0 : 6;
    unsigned char f : 1;
} S;

void fn_41_2AFDC(S* s, unsigned char v) {
    s->f = v;
}
