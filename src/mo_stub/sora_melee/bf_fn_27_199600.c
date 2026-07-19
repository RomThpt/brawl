typedef struct {
    char pad[8];
    unsigned int f : 3;
} S;

void fn_27_199600(S* p, int v) {
    p->f = v;
}
