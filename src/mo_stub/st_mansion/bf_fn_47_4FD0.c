typedef struct {
    char pad[8];
    unsigned int f : 4;
} S;

void fn_47_4FD0(S* p, int v) {
    p->f = v;
}
