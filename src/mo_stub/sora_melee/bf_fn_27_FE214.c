typedef struct {
    char pad[8];
    int f : 6;
} S;

int fn_27_FE214(S* p) {
    return p->f;
}
