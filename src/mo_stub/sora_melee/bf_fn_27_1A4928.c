typedef struct {
    char pad[8];
    unsigned int p0 : 30;
    unsigned int f : 1;
} S;

unsigned int fn_27_1A4928(S* p) {
    return p->f;
}
