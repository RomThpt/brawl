typedef struct {
    char pad[8];
    unsigned int f : 7;
} S;

void fn_48_B7C0(S* p, int v) {
    p->f = v;
}
