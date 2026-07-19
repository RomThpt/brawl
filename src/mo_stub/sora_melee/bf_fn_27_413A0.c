typedef struct {
    char pad[156];
    unsigned int p0 : 3;
    unsigned int f : 1;
} S;

void fn_27_413A0(S* p, int v) {
    p->f = v;
}
