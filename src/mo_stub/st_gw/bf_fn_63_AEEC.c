typedef struct {
    char pad[8];
    unsigned int f : 4;
} S;

void fn_63_AEEC(S* p, int v) {
    p->f = v;
}
