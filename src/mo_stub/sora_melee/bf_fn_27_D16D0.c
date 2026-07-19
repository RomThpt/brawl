typedef struct {
    char pad[8];
    unsigned int p0 : 16;
    int f : 8;
} S;

int fn_27_D16D0(S* p) {
    return p->f;
}
