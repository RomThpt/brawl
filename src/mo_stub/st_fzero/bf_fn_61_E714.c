typedef struct {
    char pad[8];
    unsigned int p0 : 3;
    int f : 3;
} S;

int fn_61_E714(S* p) {
    return p->f;
}
