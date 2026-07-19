typedef struct {
    char pad[8];
    unsigned int p0 : 4;
    int f : 4;
} S;

int fn_49_6EEC(S* p) {
    return p->f;
}
