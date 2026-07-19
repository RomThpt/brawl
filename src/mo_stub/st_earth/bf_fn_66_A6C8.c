typedef struct {
    char pad[8];
    unsigned int f : 4;
} S;

void fn_66_A6C8(S* p, int v) {
    p->f = v;
}
