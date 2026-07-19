typedef struct {
    char pad[8];
    unsigned int f : 5;
} S;

void fn_76_3CEC(S* p, int v) {
    p->f = v;
}
