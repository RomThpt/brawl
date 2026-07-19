typedef struct {
    char pad[8];
    unsigned int p0 : 3;
    int f : 3;
} S;

int fn_72_BEC0(S* p) {
    return p->f;
}
