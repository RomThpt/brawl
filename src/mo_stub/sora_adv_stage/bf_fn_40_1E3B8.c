typedef struct {
    char pad[8];
    unsigned int p0 : 12;
    int f : 6;
} S;

int fn_40_1E3B8(S* p) {
    return p->f;
}
