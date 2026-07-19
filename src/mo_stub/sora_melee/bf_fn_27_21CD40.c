typedef struct {
    char pad[4];
    unsigned int p0 : 21;
    int f : 7;
} S;

int fn_27_21CD40(S* p) {
    return p->f;
}
