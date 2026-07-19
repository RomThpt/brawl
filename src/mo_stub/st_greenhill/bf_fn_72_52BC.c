typedef struct {
    char pad[8];
    unsigned int f : 4;
} S;

void fn_72_52BC(S* p, int v) {
    p->f = v;
}
