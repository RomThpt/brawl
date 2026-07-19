typedef struct {
    char pad[8];
    unsigned int p0 : 6;
    unsigned int f : 1;
} S;

void fn_27_2648E4(S* p) {
    p->f = 1;
}
