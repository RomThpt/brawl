typedef struct {
    char pad[8];
    unsigned int p0 : 8;
    int f : 4;
} S;

int fn_40_289D0(S* p) {
    return p->f;
}
