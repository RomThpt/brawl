typedef struct {
    char pad[8];
    unsigned int p0 : 15;
    unsigned int f : 1;
} S;

unsigned int fn_27_19B100(S* p) {
    return p->f;
}
