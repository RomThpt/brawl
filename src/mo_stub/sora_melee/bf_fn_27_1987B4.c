typedef struct {
    char pad[8];
    int f : 2;
} S;

int fn_27_1987B4(S* p) {
    return p->f;
}
