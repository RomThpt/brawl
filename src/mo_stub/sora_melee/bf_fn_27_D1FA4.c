typedef struct {
    char pad[8];
    unsigned int p0 : 12;
    unsigned int f : 1;
} S;

unsigned int fn_27_D1FA4(S* p) {
    return p->f;
}
