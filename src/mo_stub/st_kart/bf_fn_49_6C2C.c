typedef struct {
    char pad[8];
    unsigned int p0 : 2;
    int f : 2;
} S;

int fn_49_6C2C(S* p) {
    return p->f;
}
