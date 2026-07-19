typedef struct {
    char pad[8];
    unsigned int p0 : 4;
    int f : 2;
} S;

int fn_74_69B8(S* p) {
    return p->f;
}
