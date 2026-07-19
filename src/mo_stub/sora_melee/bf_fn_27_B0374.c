typedef struct {
    char pad[8];
    unsigned int p0 : 9;
    int f : 9;
} S;

int fn_27_B0374(S* p) {
    return p->f;
}
