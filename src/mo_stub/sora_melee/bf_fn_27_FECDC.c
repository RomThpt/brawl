typedef struct {
    char pad[8];
    unsigned int p0 : 14;
    unsigned int f : 7;
} S;

void fn_27_FECDC(S* p, int v) {
    p->f = v;
}
