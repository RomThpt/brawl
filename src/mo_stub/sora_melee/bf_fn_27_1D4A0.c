typedef struct {
    char pad[8];
    unsigned int f : 2;
} S;

void fn_27_1D4A0(S* p, int v) {
    p->f = v;
}
