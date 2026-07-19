typedef struct {
    char pad[8];
    unsigned int p0 : 10;
    int f : 10;
} S;

int fn_27_1A6750(S* p) {
    return p->f;
}
