typedef struct {
    char pad[8];
    unsigned int p0 : 9;
    unsigned int f : 1;
} S;

unsigned int fn_27_1A0258(S* p) {
    return p->f;
}
