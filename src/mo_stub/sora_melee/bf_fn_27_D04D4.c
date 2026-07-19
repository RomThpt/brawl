typedef struct {
    char pad[8];
    unsigned int f : 7;
} S;

void fn_27_D04D4(S* p, int v) {
    p->f = v;
}
