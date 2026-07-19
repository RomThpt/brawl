typedef struct {
    char pad[8];
    unsigned int f : 4;
} S;

void fn_77_3D1C(S* p, int v) {
    p->f = v;
}
