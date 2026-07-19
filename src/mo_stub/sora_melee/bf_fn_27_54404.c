typedef struct {
    char pad[8];
    unsigned int p0 : 27;
    unsigned int f : 1;
} S;

void fn_27_54404(S* p) {
    p->f = 0;
}
