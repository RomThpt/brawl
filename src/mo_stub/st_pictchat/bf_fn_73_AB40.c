typedef struct {
    char pad[8];
    unsigned int f : 3;
} S;

void fn_73_AB40(S* p, int v) {
    p->f = v;
}
