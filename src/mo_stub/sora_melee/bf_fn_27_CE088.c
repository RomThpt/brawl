typedef struct {
    char pad[8];
    unsigned int p0 : 24;
    unsigned int f : 1;
} S;

unsigned int fn_27_CE088(S* p) {
    return p->f;
}
