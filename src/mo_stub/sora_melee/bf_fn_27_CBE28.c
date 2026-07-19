typedef struct {
    char pad[8];
    int f : 4;
} S;

int fn_27_CBE28(S* p) {
    return p->f;
}
