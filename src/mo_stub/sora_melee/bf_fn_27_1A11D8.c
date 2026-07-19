typedef struct {
    char pad[8];
    unsigned int p0 : 15;
    unsigned int f : 1;
} S;

void fn_27_1A11D8(S* p) {
    p->f = 0;
}
