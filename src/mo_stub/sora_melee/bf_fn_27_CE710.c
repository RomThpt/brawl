typedef struct {
    char pad[8];
    unsigned int p0 : 18;
    unsigned int f : 9;
} S;

void fn_27_CE710(S* p, int v) {
    p->f = v;
}
