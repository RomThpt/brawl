typedef struct {
    char pad[8];
    unsigned int p0 : 6;
    unsigned int f : 6;
} S;

void fn_79_5760(S* p, int v) {
    p->f = v;
}
