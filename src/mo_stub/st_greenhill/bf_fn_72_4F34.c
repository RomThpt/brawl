typedef struct {
    char pad[8];
    unsigned int f : 2;
} S;

void fn_72_4F34(S* p, int v) {
    p->f = v;
}
