typedef struct {
    char pad[8];
    int f : 5;
} S;

int fn_27_CC440(S* p) {
    return p->f;
}
