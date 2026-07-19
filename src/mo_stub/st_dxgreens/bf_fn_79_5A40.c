typedef struct {
    char pad[8];
    unsigned int p0 : 2;
    int f : 2;
} S;

int fn_79_5A40(S* p) {
    return p->f;
}
