typedef struct {
    char pad[8];
    unsigned int p0 : 2;
    unsigned int f : 2;
} S;

void fn_27_CCA18(S* p, int v) {
    p->f = v;
}
