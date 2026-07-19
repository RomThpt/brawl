typedef struct {
    char pad[8];
    int f : 2;
} S;

int fn_71_A018(S* p) {
    return p->f;
}
