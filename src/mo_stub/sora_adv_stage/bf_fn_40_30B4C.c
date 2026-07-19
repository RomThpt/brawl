typedef struct {
    char pad[8];
    unsigned int p0 : 15;
    unsigned int f : 1;
} S;

void fn_40_30B4C(S* p) {
    p->f = 0;
}
