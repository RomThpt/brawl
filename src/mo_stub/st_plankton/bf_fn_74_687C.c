typedef struct {
    char pad[8];
    unsigned int f : 2;
} S;

void fn_74_687C(S* p, int v) {
    p->f = v;
}
