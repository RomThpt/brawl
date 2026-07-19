typedef struct {
    char pad[8];
    int f : 2;
} S;

int fn_70_8F84(S* p) {
    return p->f;
}
