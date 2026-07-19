typedef struct {
    char pad[8];
    unsigned int f : 4;
} S;

void fn_56_66C0(S* p, int v) {
    p->f = v;
}
