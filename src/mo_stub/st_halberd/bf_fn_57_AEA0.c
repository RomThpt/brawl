typedef struct {
    char pad[8];
    unsigned int p0 : 8;
    int f : 4;
} S;

int fn_57_AEA0(S* p) {
    return p->f;
}
