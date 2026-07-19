typedef struct {
    char pad[8];
    unsigned int f : 2;
} S;

void fn_50_6350(S* p, int v) {
    p->f = v;
}
