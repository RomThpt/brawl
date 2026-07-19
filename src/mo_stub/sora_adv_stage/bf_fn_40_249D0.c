typedef struct {
    char pad[8];
    unsigned int f : 2;
} S;

void fn_40_249D0(S* p, int v) {
    p->f = v;
}
