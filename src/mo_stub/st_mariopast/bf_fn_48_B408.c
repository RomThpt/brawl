typedef struct {
    char pad[8];
    unsigned int f : 9;
} S;

void fn_48_B408(S* p, int v) {
    p->f = v;
}
