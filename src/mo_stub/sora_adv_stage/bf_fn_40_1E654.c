typedef struct {
    char pad[8];
    unsigned int p0 : 4;
    unsigned int f : 4;
} S;

void fn_40_1E654(S* p, int v) {
    p->f = v;
}
