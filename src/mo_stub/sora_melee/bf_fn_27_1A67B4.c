typedef struct {
    char pad[8];
    unsigned int p0 : 20;
    int f : 10;
} S;

int fn_27_1A67B4(S* p) {
    return p->f;
}
