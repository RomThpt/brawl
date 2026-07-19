typedef struct {
    char pad[8];
    unsigned int p0 : 21;
    unsigned int f : 1;
} S;

unsigned int fn_27_14F370(S* p) {
    return p->f;
}
