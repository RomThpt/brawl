typedef struct {
    char pad[8];
    unsigned int p0 : 30;
    unsigned int f : 1;
} S;

void fn_27_1A460C(S* p) {
    p->f = 0;
}
