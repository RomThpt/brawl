typedef struct {
    char pad[8];
    unsigned int f : 6;
} S;

void fn_79_569C(S* p, int v) {
    p->f = v;
}
