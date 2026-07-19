typedef struct {
    char pad[8];
    unsigned int p0 : 7;
    int f : 7;
} S;

int fn_27_1A4AE0(S* p) {
    return p->f;
}
