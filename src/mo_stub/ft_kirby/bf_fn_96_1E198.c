typedef struct {
    char pad[8];
    unsigned int p0 : 6;
    int f : 6;
} S;

int fn_96_1E198(S* p) {
    return p->f;
}
