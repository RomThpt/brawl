typedef struct {
    char pad[8];
    unsigned int p0 : 30;
    unsigned int f : 1;
} S;

unsigned int fn_27_1A3BF4(S* p) {
    return p->f;
}
