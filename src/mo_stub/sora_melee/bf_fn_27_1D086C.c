typedef struct {
    char pad[8];
    unsigned int p0 : 12;
    unsigned int f : 1;
} S;

unsigned int fn_27_1D086C(S* p) {
    return p->f;
}
