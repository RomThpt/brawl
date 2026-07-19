typedef struct {
    char pad[8];
    unsigned int p0 : 18;
    unsigned int f : 1;
} S;

unsigned int fn_27_CF6DC(S* p) {
    return p->f;
}
