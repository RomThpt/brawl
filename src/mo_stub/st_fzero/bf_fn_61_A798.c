typedef struct {
    char pad[8];
    unsigned int f : 4;
} S;

void fn_61_A798(S* p, int v) {
    p->f = v;
}
