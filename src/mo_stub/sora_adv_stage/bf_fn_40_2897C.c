typedef struct {
    char pad[8];
    unsigned int p0 : 4;
    unsigned int f : 4;
} S;

void fn_40_2897C(S* p, int v) {
    p->f = v;
}
