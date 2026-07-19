typedef struct {
    char pad[8];
    unsigned int p0 : 4;
    unsigned int f : 2;
} S;

void fn_71_A0D0(S* p, int v) {
    p->f = v;
}
