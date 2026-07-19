typedef struct {
    char pad[8];
    unsigned int f : 4;
} S;

void fn_49_6EDC(S* p, int v) {
    p->f = v;
}
