typedef struct {
    char pad[8];
    unsigned int p0 : 6;
    unsigned int f : 1;
} S;

void fn_77_3C0C(S* p) {
    p->f = 0;
}
