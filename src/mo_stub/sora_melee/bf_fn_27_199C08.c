typedef struct {
    char pad[8];
    unsigned int f : 5;
} S;

void fn_27_199C08(S* p, int v) {
    p->f = v;
}
