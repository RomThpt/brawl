typedef struct {
    char pad[8];
    unsigned int f : 6;
} S;

void fn_79_598C(S* p, int v) {
    p->f = v;
}
