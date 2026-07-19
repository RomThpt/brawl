typedef struct {
    char pad[4];
    unsigned int p0 : 9;
    int f : 3;
} S;

int fn_27_2AC3E8(S* p) {
    return p->f;
}
