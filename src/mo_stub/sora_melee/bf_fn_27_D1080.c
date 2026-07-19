typedef struct {
    char pad[8];
    unsigned int p0 : 16;
    unsigned int f : 8;
} S;

void fn_27_D1080(S* p, int v) {
    p->f = v;
}
