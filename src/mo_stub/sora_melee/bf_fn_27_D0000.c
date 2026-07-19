typedef struct {
    char pad[8];
    int f : 7;
} S;

int fn_27_D0000(S* p) {
    return p->f;
}
