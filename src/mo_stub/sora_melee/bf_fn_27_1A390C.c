typedef struct {
    char pad[8];
    unsigned int p0 : 20;
    unsigned int f : 10;
} S;

void fn_27_1A390C(S* p, int v) {
    p->f = v;
}
