typedef struct {
    char pad[8];
    unsigned int p0 : 3;
    int f : 3;
} S;

int fn_62_56F0(S* p) {
    return p->f;
}
