typedef struct {
    char pad[8];
    unsigned int f : 3;
} S;

void fn_51_DA14(S* p, int v) {
    p->f = v;
}
