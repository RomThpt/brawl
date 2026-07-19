typedef struct {
    char pad[8];
    unsigned int p0 : 27;
    unsigned int f : 1;
} S;

unsigned int fn_27_54414(S* p) {
    return p->f;
}
