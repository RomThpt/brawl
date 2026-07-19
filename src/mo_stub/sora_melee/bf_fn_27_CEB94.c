typedef struct {
    char pad[8];
    unsigned int p0 : 18;
    unsigned int f : 1;
} S;

void fn_27_CEB94(S* p) {
    p->f = 1;
}
