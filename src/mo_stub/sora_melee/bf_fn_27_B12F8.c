typedef struct {
    char pad[8];
    unsigned int f : 5;
} S;

void fn_27_B12F8(S* p, int v) {
    p->f = v;
}
