typedef struct {
    char pad[8];
    unsigned int p0 : 8;
    int f : 8;
} S;

int fn_27_CE1D4(S* p) {
    return p->f;
}
