typedef struct {
    char pad[8];
    unsigned int f : 2;
} S;

void fn_56_64BC(S* p, int v) {
    p->f = v;
}
