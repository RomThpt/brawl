typedef struct {
    char pad[8];
    unsigned int p0 : 12;
    unsigned int f : 1;
} S;

unsigned int fn_27_1E7E78(S* p) {
    return p->f;
}
