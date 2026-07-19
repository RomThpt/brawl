typedef struct {
    char pad[8];
    unsigned int p0 : 6;
    unsigned int f : 3;
} S;

void fn_61_E7C0(S* p, int v) {
    p->f = v;
}
