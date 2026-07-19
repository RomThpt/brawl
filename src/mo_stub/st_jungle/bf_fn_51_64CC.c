typedef struct {
    char pad[8];
    unsigned int f : 2;
} S;

void fn_51_64CC(S* p, int v) {
    p->f = v;
}
