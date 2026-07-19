typedef struct {
    char pad[8];
    unsigned int p0 : 6;
    int f : 6;
} S;

int fn_40_1E41C(S* p) {
    return p->f;
}
