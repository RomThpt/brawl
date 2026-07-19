typedef struct {
    char pad[8];
    unsigned int p0 : 6;
    unsigned int f : 6;
} S;

void fn_96_1E1A8(S* p, int v) {
    p->f = v;
}
