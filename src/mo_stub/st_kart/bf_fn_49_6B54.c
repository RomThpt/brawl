typedef struct {
    char pad[8];
    unsigned int f : 2;
} S;

void fn_49_6B54(S* p, int v) {
    p->f = v;
}
