typedef struct {
    char pad[8];
    unsigned int p0 : 9;
    unsigned int f : 1;
} S;

void fn_27_19A798(S* p) {
    p->f = 0;
}
