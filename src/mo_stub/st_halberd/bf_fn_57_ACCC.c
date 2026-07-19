typedef struct {
    char pad[8];
    unsigned int f : 2;
} S;

void fn_57_ACCC(S* p, int v) {
    p->f = v;
}
