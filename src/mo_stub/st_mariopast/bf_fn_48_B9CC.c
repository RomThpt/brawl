typedef struct {
    char pad[8];
    unsigned int p0 : 14;
    unsigned int f : 7;
} S;

void fn_48_B9CC(S* p, int v) {
    p->f = v;
}
