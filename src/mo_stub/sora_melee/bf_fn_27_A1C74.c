typedef struct {
    char pad[8];
    unsigned int p0 : 10;
    unsigned int f : 5;
} S;

void fn_27_A1C74(S* p, int v) {
    p->f = v;
}
