typedef struct {
    char pad[8];
    unsigned int p0 : 12;
    unsigned int f : 1;
} S;

void fn_27_D2CDC(S* p) {
    p->f = 0;
}
