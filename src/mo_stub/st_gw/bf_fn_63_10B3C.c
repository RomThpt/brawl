typedef struct {
    char pad[8];
    unsigned int p0 : 4;
    int f : 2;
} S;

int fn_63_10B3C(S* p) {
    return p->f;
}
