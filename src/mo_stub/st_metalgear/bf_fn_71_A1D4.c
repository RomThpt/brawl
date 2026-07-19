typedef struct {
    char pad[8];
    unsigned int p0 : 12;
    unsigned int f : 1;
} S;

void fn_71_A1D4(S* p) {
    p->f = 0;
}
