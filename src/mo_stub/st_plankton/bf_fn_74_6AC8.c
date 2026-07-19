typedef struct {
    char pad[8];
    unsigned int f : 2;
} S;

void fn_74_6AC8(S* p, int v) {
    p->f = v;
}
