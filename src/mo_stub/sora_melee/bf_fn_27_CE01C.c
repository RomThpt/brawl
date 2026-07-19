typedef struct {
    char pad[8];
    int f : 8;
} S;

int fn_27_CE01C(S* p) {
    return p->f;
}
