typedef struct {
    char pad[8];
    unsigned int f : 2;
} S;

void fn_73_ABE4(S* p, int v) {
    p->f = v;
}
