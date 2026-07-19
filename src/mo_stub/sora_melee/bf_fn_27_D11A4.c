typedef struct {
    char pad[8];
    unsigned int p0 : 8;
    int f : 8;
} S;

int fn_27_D11A4(S* p) {
    return p->f;
}
