typedef struct {
    char pad[8];
    unsigned int p0 : 2;
    int f : 2;
} S;

int fn_78_4D60(S* p) {
    return p->f;
}
