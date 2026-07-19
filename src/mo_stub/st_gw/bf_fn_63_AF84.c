typedef struct {
    char pad[8];
    int f : 2;
} S;

int fn_63_AF84(S* p) {
    return p->f;
}
