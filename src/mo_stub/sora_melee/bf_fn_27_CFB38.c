typedef struct {
    char pad[8];
    int f : 6;
} S;

int fn_27_CFB38(S* p) {
    return p->f;
}
