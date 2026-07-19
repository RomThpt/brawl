typedef struct {
    char pad[8];
    unsigned int p0 : 12;
    unsigned int f : 6;
} S;

void fn_27_296214(S* p, int v) {
    p->f = v;
}
