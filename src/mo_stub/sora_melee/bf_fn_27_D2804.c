typedef struct {
    char pad[8];
    unsigned int f : 5;
} S;

void fn_27_D2804(S* p, int v) {
    p->f = v;
}
