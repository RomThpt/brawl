typedef struct {
    char pad[8];
    unsigned int p0 : 8;
    int f : 8;
} S;

int fn_27_D166C(S* p) {
    return p->f;
}
