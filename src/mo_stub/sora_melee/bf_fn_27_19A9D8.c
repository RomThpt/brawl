typedef struct {
    char pad[8];
    unsigned int p0 : 3;
    int f : 3;
} S;

int fn_27_19A9D8(S* p) {
    return p->f;
}
