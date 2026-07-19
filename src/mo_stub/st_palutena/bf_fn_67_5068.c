typedef struct {
    char pad[8];
    unsigned int p0 : 4;
    int f : 2;
} S;

int fn_67_5068(S* p) {
    return p->f;
}
