typedef struct {
    char pad[8];
    unsigned int f : 6;
} S;

void fn_40_1E40C(S* p, int v) {
    p->f = v;
}
