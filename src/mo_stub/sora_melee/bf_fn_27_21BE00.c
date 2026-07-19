typedef struct {
    char pad[4];
    unsigned int p0 : 24;
    int f : 8;
} S;

int fn_27_21BE00(S* p) {
    return p->f;
}
