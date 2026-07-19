typedef struct {
    char pad[8];
    unsigned int f : 7;
} S;

void fn_48_B944(S* p, int v) {
    p->f = v;
}
