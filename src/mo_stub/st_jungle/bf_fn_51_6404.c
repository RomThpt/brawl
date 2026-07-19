typedef struct {
    char pad[8];
    unsigned int f : 2;
} S;

void fn_51_6404(S* p, int v) {
    p->f = v;
}
