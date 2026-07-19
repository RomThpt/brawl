typedef struct {
    char pad[8];
    unsigned int p0 : 8;
    unsigned int f : 8;
} S;

void fn_27_D167C(S* p, int v) {
    p->f = v;
}
