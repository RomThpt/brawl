typedef struct {
    char pad[8];
    unsigned int p0 : 12;
    unsigned int f : 6;
} S;

void fn_27_1992E4(S* p, int v) {
    p->f = v;
}
