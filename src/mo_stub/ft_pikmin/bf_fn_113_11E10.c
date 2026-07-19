typedef struct {
    char pad[8];
    unsigned int p0 : 2;
    int f : 2;
} S;

int fn_113_11E10(S* p) {
    return p->f;
}
