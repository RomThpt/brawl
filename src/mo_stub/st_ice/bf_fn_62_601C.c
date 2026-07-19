typedef struct {
    char pad[8];
    int f : 2;
} S;

int fn_62_601C(S* p) {
    return p->f;
}
