typedef struct {
    char pad[8];
    unsigned int p0 : 4;
    unsigned int f : 2;
} S;

void fn_27_C9B0C(S* p, int v) {
    p->f = v;
}
