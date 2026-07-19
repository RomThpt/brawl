typedef struct {
    char pad[8];
    unsigned int p0 : 12;
    unsigned int f : 6;
} S;

void fn_27_AC36C(S* p, int v) {
    p->f = v;
}
