typedef struct {
    char pad[8];
    unsigned int p0 : 9;
    int f : 9;
} S;

int fn_48_B5A8(S* p) {
    return p->f;
}
