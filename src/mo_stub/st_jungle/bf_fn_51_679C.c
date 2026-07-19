typedef struct {
    char pad[8];
    unsigned int p0 : 4;
    int f : 4;
} S;

int fn_51_679C(S* p) {
    return p->f;
}
