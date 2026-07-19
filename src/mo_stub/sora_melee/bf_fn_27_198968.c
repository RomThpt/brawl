typedef struct {
    char pad[8];
    unsigned int p0 : 3;
    int f : 3;
} S;

int fn_27_198968(S* p) {
    return p->f;
}
