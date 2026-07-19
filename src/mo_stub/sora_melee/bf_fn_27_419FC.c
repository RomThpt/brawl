typedef struct {
    char pad[8];
    unsigned int f : 4;
} S;

void fn_27_419FC(S* p, int v) {
    p->f = v;
}
