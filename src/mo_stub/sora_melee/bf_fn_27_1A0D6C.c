typedef struct {
    char pad[8];
    unsigned int p0 : 6;
    int f : 3;
} S;

int fn_27_1A0D6C(S* p) {
    return p->f;
}
