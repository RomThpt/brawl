typedef struct {
    char pad[8];
    unsigned int p0 : 4;
    unsigned int f : 2;
} S;

void fn_113_11EAC(S* p, int v) {
    p->f = v;
}
