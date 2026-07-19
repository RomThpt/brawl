typedef struct {
    char pad[8];
    unsigned int p0 : 5;
    unsigned int f : 5;
} S;

void fn_40_30D28(S* p, int v) {
    p->f = v;
}
