typedef struct {
    char pad[8];
    unsigned int p0 : 5;
    int f : 5;
} S;

int fn_27_A1BD8(S* p) {
    return p->f;
}
