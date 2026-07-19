typedef struct {
    char pad[8];
    unsigned int f : 6;
} S;

void fn_27_D1C4C(S* p, int v) {
    p->f = v;
}
