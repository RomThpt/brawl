typedef struct {
    char pad[8];
    unsigned int p0 : 18;
    unsigned int f : 1;
} S;

unsigned int fn_27_19F268(S* p) {
    return p->f;
}
