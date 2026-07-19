typedef struct {
    char pad[8];
    unsigned int p0 : 18;
    int f : 9;
} S;

int fn_48_B47C(S* p) {
    return p->f;
}
