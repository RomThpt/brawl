typedef struct {
    char pad[8];
    unsigned int p0 : 4;
    int f : 2;
} S;

int fn_70_90CC(S* p) {
    return p->f;
}
