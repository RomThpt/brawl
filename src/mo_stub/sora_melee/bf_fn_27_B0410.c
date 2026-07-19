typedef struct {
    char pad[8];
    int f : 5;
} S;

int fn_27_B0410(S* p) {
    return p->f;
}
