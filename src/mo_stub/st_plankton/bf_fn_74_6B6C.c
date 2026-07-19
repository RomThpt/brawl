typedef struct {
    char pad[8];
    unsigned int f : 4;
} S;

void fn_74_6B6C(S* p, int v) {
    p->f = v;
}
