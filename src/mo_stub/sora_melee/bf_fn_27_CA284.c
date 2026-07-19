typedef struct {
    char pad[8];
    unsigned int f : 5;
} S;

void fn_27_CA284(S* p, int v) {
    p->f = v;
}
