typedef struct {
    char pad[8];
    unsigned int p0 : 15;
    unsigned int f : 1;
} S;

void fn_27_1A21A0(S* p) {
    p->f = 1;
}
