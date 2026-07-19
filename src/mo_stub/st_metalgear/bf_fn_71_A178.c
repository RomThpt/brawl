typedef struct {
    char pad[8];
    int f : 4;
} S;

int fn_71_A178(S* p) {
    return p->f;
}
