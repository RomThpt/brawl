typedef struct {
    char pad[8];
    unsigned int f : 4;
} S;

void fn_27_1A26A0(S* p, int v) {
    p->f = v;
}
