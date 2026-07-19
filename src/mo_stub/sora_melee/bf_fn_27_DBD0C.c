typedef struct {
    char pad[8];
    unsigned int p0 : 4;
    int f : 2;
} S;

int fn_27_DBD0C(S* p) {
    return p->f;
}
