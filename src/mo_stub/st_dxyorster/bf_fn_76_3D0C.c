typedef struct {
    char pad[8];
    unsigned int p0 : 5;
    unsigned int f : 5;
} S;

void fn_76_3D0C(S* p, int v) {
    p->f = v;
}
