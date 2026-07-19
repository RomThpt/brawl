typedef struct {
    char pad[8];
    unsigned int p0 : 10;
    unsigned int f : 5;
} S;

void fn_27_11B9C0(S* p, int v) {
    p->f = v;
}
