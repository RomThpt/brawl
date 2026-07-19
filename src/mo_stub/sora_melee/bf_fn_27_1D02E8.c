typedef struct {
    char pad[8];
    unsigned int p0 : 14;
    unsigned int f : 7;
} S;

void fn_27_1D02E8(S* p, int v) {
    p->f = v;
}
