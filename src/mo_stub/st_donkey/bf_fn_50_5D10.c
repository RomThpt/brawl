typedef struct {
    char pad[8];
    int f : 2;
} S;

int fn_50_5D10(S* p) {
    return p->f;
}
