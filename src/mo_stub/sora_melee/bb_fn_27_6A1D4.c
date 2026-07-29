typedef struct {
    char pad[52];
    unsigned char p0 : 6;
    unsigned char f : 1;
} S;

void fn_27_6A1D4(S* s, unsigned char v) {
    s->f = v;
}
