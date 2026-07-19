typedef struct {
    char pad[8];
    unsigned int p0 : 12;
    unsigned int f : 1;
} S;

unsigned int fn_27_3957C8(S* p) {
    return p->f;
}
