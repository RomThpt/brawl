typedef struct {
    char pad[8];
    unsigned int f : 3;
} S;

void fn_72_BEE4(S* p, int v) {
    p->f = v;
}
