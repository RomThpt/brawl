typedef struct {
    char pad[8];
    unsigned int p0 : 4;
    int f : 4;
} S;

int fn_50_6404(S* p) {
    return p->f;
}
