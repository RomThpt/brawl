typedef struct {
    char pad[8];
    unsigned int f : 2;
} S;

void fn_27_AE61C(S* p, int v) {
    p->f = v;
}
