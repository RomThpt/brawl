typedef struct {
    char pad[8];
    unsigned int p0 : 15;
    unsigned int f : 1;
} S;

void fn_27_1CFCCC(S* p) {
    p->f = 1;
}
