typedef struct {
    char pad[8];
    unsigned int p0 : 9;
    unsigned int f : 9;
} S;

void fn_27_CE6AC(S* p, int v) {
    p->f = v;
}
