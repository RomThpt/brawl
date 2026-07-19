typedef struct {
    char pad[8];
    unsigned int p0 : 10;
    unsigned int f : 10;
} S;

void fn_27_1A3CB8(S* p, int v) {
    p->f = v;
}
