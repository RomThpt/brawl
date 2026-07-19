typedef struct {
    char pad[8];
    unsigned int p0 : 5;
    unsigned int f : 5;
} S;

void fn_27_B043C(S* p, int v) {
    p->f = v;
}
