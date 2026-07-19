typedef struct {
    char pad[8];
    unsigned int f : 2;
} S;

void fn_27_1A2B54(S* p, int v) {
    p->f = v;
}
