typedef struct {
    char pad[8];
    unsigned int f : 5;
} S;

void fn_40_30A34(S* p, int v) {
    p->f = v;
}
