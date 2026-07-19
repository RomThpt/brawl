typedef struct {
    char pad[8];
    unsigned int f : 7;
} S;

void fn_27_1D0C5C(S* p, int v) {
    p->f = v;
}
