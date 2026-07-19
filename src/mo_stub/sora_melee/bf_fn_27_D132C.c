typedef struct {
    char pad[8];
    unsigned int f : 8;
} S;

void fn_27_D132C(S* p, int v) {
    p->f = v;
}
