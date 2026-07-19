typedef struct {
    char pad[8];
    unsigned int p0 : 9;
    unsigned int f : 9;
} S;

void fn_27_5430C(S* p, int v) {
    p->f = v;
}
