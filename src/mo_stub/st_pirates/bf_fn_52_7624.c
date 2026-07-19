typedef struct {
    char pad[8];
    unsigned int f : 4;
} S;

void fn_52_7624(S* p, int v) {
    p->f = v;
}
