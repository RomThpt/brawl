typedef struct {
    char pad[8];
    unsigned int p0 : 6;
    unsigned int f : 6;
} S;

void fn_27_1D0D34(S* p, int v) {
    p->f = v;
}
