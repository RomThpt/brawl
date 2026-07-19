typedef struct {
    char pad[8];
    unsigned int p0 : 4;
    int f : 2;
} S;

int fn_72_5070(S* p) {
    return p->f;
}
