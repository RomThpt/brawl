typedef struct {
    char pad[8];
    unsigned int f : 9;
} S;

void fn_27_B0364(S* p, int v) {
    p->f = v;
}
