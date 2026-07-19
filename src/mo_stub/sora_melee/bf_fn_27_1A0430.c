typedef struct {
    char pad[8];
    unsigned int p0 : 21;
    unsigned int f : 1;
} S;

void fn_27_1A0430(S* p) {
    p->f = 0;
}
