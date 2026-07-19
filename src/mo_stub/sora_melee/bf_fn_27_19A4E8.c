typedef struct {
    char pad[8];
    unsigned int p0 : 5;
    unsigned int f : 5;
} S;

void fn_27_19A4E8(S* p, int v) {
    p->f = v;
}
