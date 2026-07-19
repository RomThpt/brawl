typedef struct {
    char pad[8];
    unsigned int p0 : 10;
    unsigned int f : 10;
} S;

void fn_27_1A6A6C(S* p, int v) {
    p->f = v;
}
