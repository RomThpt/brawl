typedef struct {
    char pad[8];
    unsigned int p0 : 4;
    unsigned int f : 2;
} S;

void fn_51_64B0(S* p, int v) {
    p->f = v;
}
