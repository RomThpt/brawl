typedef struct {
    char pad[8];
    unsigned int p0 : 5;
    unsigned int f : 5;
} S;

void fn_76_3DD4(S* p, int v) {
    p->f = v;
}
