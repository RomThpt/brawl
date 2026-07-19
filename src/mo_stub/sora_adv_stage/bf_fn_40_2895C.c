typedef struct {
    char pad[8];
    unsigned int f : 4;
} S;

void fn_40_2895C(S* p, int v) {
    p->f = v;
}
