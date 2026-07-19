typedef struct {
    char pad[8];
    unsigned int f : 2;
} S;

void fn_66_A3FC(S* p, int v) {
    p->f = v;
}
