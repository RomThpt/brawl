typedef struct {
    char pad[8];
    unsigned int p0 : 24;
    unsigned int f : 1;
} S;

void fn_27_CE068(S* p) {
    p->f = 1;
}
