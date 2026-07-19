typedef struct {
    char pad[8];
    int f : 5;
} S;

int fn_27_B12EC(S* p) {
    return p->f;
}
