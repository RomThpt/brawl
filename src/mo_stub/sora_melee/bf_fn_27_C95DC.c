typedef struct {
    char pad[8];
    unsigned int p0 : 9;
    unsigned int f : 1;
} S;

void fn_27_C95DC(S* p) {
    p->f = 1;
}
