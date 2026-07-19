typedef struct {
    char pad[8];
    unsigned int p0 : 5;
    int f : 5;
} S;

int fn_27_CB0CC(S* p) {
    return p->f;
}
