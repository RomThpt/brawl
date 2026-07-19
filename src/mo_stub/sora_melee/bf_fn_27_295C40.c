typedef struct {
    char pad[8];
    unsigned int p0 : 3;
    int f : 3;
} S;

int fn_27_295C40(S* p) {
    return p->f;
}
