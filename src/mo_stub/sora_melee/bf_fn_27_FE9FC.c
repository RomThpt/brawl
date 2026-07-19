typedef struct {
    char pad[8];
    unsigned int p0 : 6;
    unsigned int f : 3;
} S;

void fn_27_FE9FC(S* p, int v) {
    p->f = v;
}
