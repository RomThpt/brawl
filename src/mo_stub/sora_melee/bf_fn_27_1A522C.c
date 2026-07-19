typedef struct {
    char pad[8];
    unsigned int p0 : 9;
    unsigned int f : 1;
} S;

void fn_27_1A522C(S* p) {
    p->f = 1;
}
