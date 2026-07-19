typedef struct {
    char pad[4];
    unsigned int p0 : 23;
    unsigned int f : 1;
} S;

unsigned int fn_10_8368(S* p) {
    return p->f;
}
