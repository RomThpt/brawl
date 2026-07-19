typedef struct {
    char pad[8];
    unsigned int f : 2;
} S;

void fn_54_6514(S* p, int v) {
    p->f = v;
}
