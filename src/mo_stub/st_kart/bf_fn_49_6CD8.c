typedef struct {
    char pad[8];
    unsigned int f : 2;
} S;

void fn_49_6CD8(S* p, int v) {
    p->f = v;
}
