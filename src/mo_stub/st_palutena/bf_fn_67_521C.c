typedef struct {
    char pad[8];
    unsigned int f : 4;
} S;

void fn_67_521C(S* p, int v) {
    p->f = v;
}
