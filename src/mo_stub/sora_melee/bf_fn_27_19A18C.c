typedef struct {
    char pad[8];
    unsigned int p0 : 10;
    unsigned int f : 5;
} S;

void fn_27_19A18C(S* p, int v) {
    p->f = v;
}
