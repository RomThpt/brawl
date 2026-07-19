typedef struct {
    char pad[8];
    int f : 5;
} S;

int fn_40_30AF0(S* p) {
    return p->f;
}
