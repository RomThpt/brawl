typedef struct {
    char pad[8];
    unsigned int p0 : 7;
    unsigned int f : 7;
} S;

void fn_27_1A0400(S* p, int v) {
    p->f = v;
}
