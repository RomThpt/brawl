typedef struct {
    char pad[8];
    int f : 4;
} S;

int fn_27_1982EC(S* p) {
    return p->f;
}
