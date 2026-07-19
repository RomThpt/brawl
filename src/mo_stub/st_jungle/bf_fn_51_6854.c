typedef struct {
    char pad[8];
    unsigned int f : 4;
} S;

void fn_51_6854(S* p, int v) {
    p->f = v;
}
