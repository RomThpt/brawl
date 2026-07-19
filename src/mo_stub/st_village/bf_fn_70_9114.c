typedef struct {
    char pad[8];
    unsigned int f : 2;
} S;

void fn_70_9114(S* p, int v) {
    p->f = v;
}
