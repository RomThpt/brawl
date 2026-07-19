typedef struct {
    char pad[8];
    unsigned int p0 : 8;
    int f : 4;
} S;

int fn_66_A674(S* p) {
    return p->f;
}
