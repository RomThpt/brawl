typedef struct {
    char pad[8];
    unsigned int p0 : 6;
    int f : 6;
} S;

int fn_27_D1C5C(S* p) {
    return p->f;
}
