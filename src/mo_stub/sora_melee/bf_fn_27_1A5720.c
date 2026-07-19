typedef struct {
    char pad[8];
    unsigned int p0 : 4;
    unsigned int f : 4;
} S;

void fn_27_1A5720(S* p, int v) {
    p->f = v;
}
