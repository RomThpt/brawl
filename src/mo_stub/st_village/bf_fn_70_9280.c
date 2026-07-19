typedef struct {
    char pad[8];
    unsigned int f : 4;
} S;

void fn_70_9280(S* p, int v) {
    p->f = v;
}
