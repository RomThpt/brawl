typedef struct {
    char pad[8];
    unsigned int p0 : 18;
    unsigned int f : 1;
} S;

void fn_27_1A31BC(S* p) {
    p->f = 0;
}
