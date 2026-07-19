typedef struct {
    char pad[8];
    unsigned int f : 2;
} S;

void fn_49_6E38(S* p, int v) {
    p->f = v;
}
