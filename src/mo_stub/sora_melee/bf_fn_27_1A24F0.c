typedef struct {
    char pad[8];
    unsigned int p0 : 15;
    unsigned int f : 1;
} S;

unsigned int fn_27_1A24F0(S* p) {
    return p->f;
}
