typedef struct {
    char pad[8];
    unsigned int p0 : 4;
    int f : 4;
} S;

int fn_56_66D0(S* p) {
    return p->f;
}
