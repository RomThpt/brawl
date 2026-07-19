typedef struct {
    char pad[8];
    unsigned int p0 : 5;
    int f : 5;
} S;

int fn_40_30C6C(S* p) {
    return p->f;
}
