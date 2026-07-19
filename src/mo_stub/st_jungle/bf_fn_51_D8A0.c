typedef struct {
    char pad[8];
    unsigned int p0 : 3;
    int f : 3;
} S;

int fn_51_D8A0(S* p) {
    return p->f;
}
