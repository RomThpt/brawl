typedef struct {
    char pad[8];
    unsigned int p0 : 7;
    unsigned int f : 7;
} S;

void fn_27_D035C(S* p, int v) {
    p->f = v;
}
