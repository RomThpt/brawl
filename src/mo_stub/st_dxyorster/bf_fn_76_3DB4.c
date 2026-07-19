typedef struct {
    char pad[8];
    unsigned int f : 5;
} S;

void fn_76_3DB4(S* p, int v) {
    p->f = v;
}
