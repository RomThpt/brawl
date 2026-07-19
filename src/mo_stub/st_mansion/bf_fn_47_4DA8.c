typedef struct {
    char pad[8];
    unsigned int f : 2;
} S;

void fn_47_4DA8(S* p, int v) {
    p->f = v;
}
