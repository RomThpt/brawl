typedef struct {
    char pad[8];
    unsigned int p0 : 4;
    int f : 4;
} S;

int fn_61_A7A8(S* p) {
    return p->f;
}
