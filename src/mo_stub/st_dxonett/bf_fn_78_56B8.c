typedef struct {
    char pad[8];
    unsigned int p0 : 2;
    unsigned int f : 2;
} S;

void fn_78_56B8(S* p, int v) {
    p->f = v;
}
