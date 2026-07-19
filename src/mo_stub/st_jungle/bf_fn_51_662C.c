typedef struct {
    char pad[8];
    unsigned int f : 2;
} S;

void fn_51_662C(S* p, int v) {
    p->f = v;
}
