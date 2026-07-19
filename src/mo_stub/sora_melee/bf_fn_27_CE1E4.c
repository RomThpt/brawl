typedef struct {
    char pad[8];
    unsigned int p0 : 8;
    unsigned int f : 8;
} S;

void fn_27_CE1E4(S* p, int v) {
    p->f = v;
}
