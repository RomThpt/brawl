typedef struct {
    char pad[8];
    unsigned int f : 6;
} S;

void fn_79_58D0(S* p, int v) {
    p->f = v;
}
