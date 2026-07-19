typedef struct {
    char pad[8];
    unsigned int p0 : 3;
    unsigned int f : 3;
} S;

void fn_51_D7E8(S* p, int v) {
    p->f = v;
}
