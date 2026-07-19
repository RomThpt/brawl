typedef struct {
    char pad[8];
    unsigned int p0 : 8;
    unsigned int f : 4;
} S;

void fn_63_B264(S* p, int v) {
    p->f = v;
}
