typedef struct {
    char pad[8];
    int f : 5;
} S;

int fn_40_30A28(S* p) {
    return p->f;
}
