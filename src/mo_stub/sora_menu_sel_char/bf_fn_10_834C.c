typedef struct {
    char pad[12];
    unsigned int p0 : 23;
    unsigned int f : 1;
} S;

unsigned int fn_10_834C(S* p) {
    return p->f;
}
