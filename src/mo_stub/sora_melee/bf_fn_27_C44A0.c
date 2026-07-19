typedef struct {
    char pad[8];
    unsigned int p0 : 6;
    int f : 6;
} S;

int fn_27_C44A0(S* p) {
    return p->f;
}
