typedef struct {
    char pad[8];
    unsigned int p0 : 6;
    unsigned int f : 3;
} S;

void fn_72_BF6C(S* p, int v) {
    p->f = v;
}
