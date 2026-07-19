typedef struct {
    char pad[8];
    unsigned int f : 2;
} S;

void fn_63_11F64(S* p, int v) {
    p->f = v;
}
