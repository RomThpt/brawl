typedef struct {
    char pad[8];
    unsigned int p0 : 12;
    unsigned int f : 1;
} S;

void fn_27_CBA5C(S* p) {
    p->f = 0;
}
