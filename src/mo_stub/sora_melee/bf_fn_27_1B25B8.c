typedef struct {
    char pad[8];
    unsigned int p0 : 4;
    int f : 2;
} S;

int fn_27_1B25B8(S* p) {
    return p->f;
}
