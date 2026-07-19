typedef struct {
    char pad[8];
    unsigned int p0 : 6;
    unsigned int f : 3;
} S;

void fn_27_1A0D7C(S* p, int v) {
    p->f = v;
}
