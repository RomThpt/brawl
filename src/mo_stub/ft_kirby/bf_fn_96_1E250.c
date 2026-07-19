typedef struct {
    char pad[8];
    unsigned int f : 4;
} S;

void fn_96_1E250(S* p, int v) {
    p->f = v;
}
