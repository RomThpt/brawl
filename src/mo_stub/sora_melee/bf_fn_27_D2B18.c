typedef struct {
    char pad[8];
    unsigned int f : 4;
} S;

void fn_27_D2B18(S* p, int v) {
    p->f = v;
}
