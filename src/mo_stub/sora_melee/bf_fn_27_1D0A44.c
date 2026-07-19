typedef struct {
    char pad[8];
    unsigned int p0 : 3;
    int f : 3;
} S;

int fn_27_1D0A44(S* p) {
    return p->f;
}
