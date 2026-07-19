typedef struct {
    char pad[8];
    unsigned int p0 : 6;
    int f : 3;
} S;

int fn_73_AB90(S* p) {
    return p->f;
}
