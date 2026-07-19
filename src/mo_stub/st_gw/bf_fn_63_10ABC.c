typedef struct {
    char pad[8];
    int f : 2;
} S;

int fn_63_10ABC(S* p) {
    return p->f;
}
