typedef struct {
    char pad[8];
    unsigned int p0 : 6;
    unsigned int f : 3;
} S;

void fn_51_DA04(S* p, int v) {
    p->f = v;
}
